import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key  # Set the API key for OpenAI

st.title("Audio Transcription and Translation")

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with open("temp_audio.mp3", "wb") as f:
        f.write(uploaded_file.read())  # Use .read() to get the file content
    
    # Select transcription or translation
    option = st.radio("Select option:", ("Transcribe (English)", "Translate (Other languages)"))
    
    if st.button("Process Audio"):
        audio_file = open("temp_audio.mp3", "rb")  # Open the temporary file in read binary mode
        
        try:
            if option == "Transcribe (English)":
                # Transcribe audio to English
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            else:
                # Translate audio to other languages
                transcript = openai.Audio.translate(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            st.write("**Transcribed/Translated Text:**")
            st.write(transcript)
        
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API Error: {e}")
        
        finally:
            audio_file.close()  # Close the file handle after processing

# Clean up: Remove temporary audio file after processing
if os.path.exists("temp_audio.mp3"):
    os.remove("temp_audio.mp3")
