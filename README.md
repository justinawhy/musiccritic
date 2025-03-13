What Are They Singing About?
a sarcastic AI MUSIC CRITIC

Summary

This is a Streamlit web app that fetches song lyrics from Genius, 
analyzes them, and provides a sarcastic music critique using an 
AI model from Hugging Face. 
The app humorously roasts an artist’s lyrics in a witty and brief manner.

Languages and Libraries Used

Python
Streamlit (for UI)
LyricsGenius (to fetch lyrics)
LangChain (for text processing)
Hugging Face API (for AI-generated summaries)
dotenv (to securely store API keys)

Key Learnings

Implementing API calls (Genius API for fetching lyrics, Hugging Face API for text generation).
Using LangChain for text processing and chunking large text.
Building a Streamlit UI for an interactive app.


Challenges Overcame

Managing long text (Splitting lyrics into chunks so they fit within the AI model’s token limit).
Writing the right AI prompts to generate the right lenght and form humorous summaries.


How to Use This App
1️⃣ Enter an artist’s name.
2️⃣ Choose how many songs to analyze.
3️⃣ Click "Summarize Lyrics" and wait for the sarcastic AI review.
