import streamlit as st
import lyricsgenius
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")
genius = lyricsgenius.Genius(GENIUS_API_KEY, remove_section_headers=True, skip_non_songs=True, timeout=10)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_KEY 


# Streamlit UI components
st.title("What are they singing about?")
artist = st.text_input("Enter the artist name:")
nb_songs = st.number_input("Enter the number of songs to summarize:", min_value=1, max_value=10, value=5)

# Fetching and displaying songs
if st.button('Summarize Lyrics'):
    if artist and nb_songs > 0:
        st.write(f"🔍 songs by {artist}")

        songs_placeholder = st.empty()

        # Fetch songs
        with st.spinner("Fetching songs and reading lyrics... Please wait a little, maybe take a look through the window and do some eye exercises 🌅"):
            artist_genius = genius.search_artist(artist, max_songs=nb_songs, sort='popularity')

        if artist_genius:
            titles = []
            lyrics = []
            
            # Song list
            output_text = ""

            for i, song in enumerate(artist_genius.songs, start=1):
                titles.append(song.title)
                lyrics.append(song.lyrics)

                # Output songs, fetched from genius API by popularity
                output_text += f"Song {i}: \"{song.title}\"\n"
                songs_placeholder.text_area("Here you go:", value=output_text, height=200, disabled=True)

            
            st.session_state["fetched_titles"] = titles

            # Combine all lyrics into one large text
            combined_lyrics = " ".join(lyrics)

            document = Document(page_content=combined_lyrics)

            # Splitting the lyrics into chunks using the text splitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=500)
            chunks = text_splitter.split_documents([document])

            # Combining chunks to ensure it fits within the model's token limit
            combined_chunks = " ".join([chunk.page_content for chunk in chunks])
            max_tokens = 4000 
            combined_chunks = combined_chunks[:max_tokens]      

            # Set up the HuggingFace model endpoint
            response = HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-Instruct-v0.3",
                task='text-generation',
                max_new_tokens=400,
                temperature=0.9,
                top_p=0.96,
                repetition_penalty=1.03
            )

            # Defining prompt template
            prompt_template = """
            You are a sarcastic and humorous music critic. Analyze ALL the lyrics together, NOT separately. 
            Summarize the general themes and your sarcastic opinion about them in a single, short paragraph. NO emojis.

            Be witty, sharp, and sarcastic, but keep it BRIEF—no numbered lists, no over-explanations. 
            Mock the lyrics in a funny and clever way. Your sarcastic opinion in 2-3 sentences. Imagine you're roasting the band.

            Here are the lyrics:
            {lyrics}

            Now, give me ONE funny and sarcastic opinion about them.
            """
        
            final_prompt = prompt_template.format(lyrics=combined_chunks)
            final_output = response.invoke(final_prompt)

            # Display the sarcastic summary
            st.text_area("Here is what I think:", value=final_output, height=300)
        
    else:
        st.warning("Please enter a valid artist name and number of songs to summarize.")
