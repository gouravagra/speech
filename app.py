import streamlit as st
from gtts import gTTS
import os
import speech_recognition as sr

# Initialize the Streamlit app
st.title("Speech-to-Text and Text-to-Speech Chatbot")
st.write("Speak into your microphone or type a message below!")

# Speech-to-Text (STT) Functionality
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak into your microphone.")
        try:
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Text-to-Speech (TTS) Functionality
def text_to_speech(text, output_file="output.mp3"):
    tts = gTTS(text)
    tts.save(output_file)
    return output_file

# STT Button
if st.button("Start Speaking"):
    result_text = speech_to_text()
    st.success(f"Recognized Text: {result_text}")

# Text Input for Chatbot
user_input = st.text_input("Type your message here:")
if user_input:
    st.info(f"You said: {user_input}")
    tts_file = text_to_speech(user_input)
    st.audio(tts_file, format="audio/mp3")
    st.success("Text converted to speech successfully!")

# Cleanup generated files
if os.path.exists("output.mp3"):
    os.remove("output.mp3")
