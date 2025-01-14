import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os

# Streamlit app title and description
st.title("Speech-to-Text and Text-to-Speech Chatbot")
st.write("Use your microphone to record audio and convert it to text. You can also type text to convert it back to speech.")

# Function to convert text to speech (TTS)
def text_to_speech(text, output_file="output.mp3"):
    tts = gTTS(text)
    tts.save(output_file)
    return output_file

# Function to convert speech to text (STT)
def speech_to_text_from_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError:
        return "Error with the speech recognition service."
    except Exception as e:
        return f"Error: {str(e)}"

# Capture audio input from the microphone
audio_uploaded_file = st.audio_input("Record your audio message:", key="audio_input")

# Placeholder for speech-to-text result
result_text = None

# Process the recorded audio
if audio_uploaded_file:
    # Save the uploaded audio temporarily
    audio_file_path = "temp_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(audio_uploaded_file.getvalue())  # Use `.getvalue()` to retrieve bytes

    st.info("Processing your audio...")
    result_text = speech_to_text_from_audio(audio_file_path)

    # Cleanup the temporary file
    os.remove(audio_file_path)

# Display recognized text if available
if result_text:
    st.success(f"Recognized Text: {result_text}")

    # Convert recognized text to speech and play it
    tts_file = text_to_speech(result_text)
    st.audio(tts_file, format="audio/mp3")
    st.success("Text converted to speech successfully!")

# Text input for chatbot
user_input = st.text_input("Or type your message here:")
if user_input:
    st.info(f"You typed: {user_input}")
    tts_file = text_to_speech(user_input)
    st.audio(tts_file, format="audio/mp3")
    st.success("Text converted to speech successfully!")
