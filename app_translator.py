import streamlit as st
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import os

# Set up the Streamlit app
st.set_page_config(page_title="Language Translater by Jagar", layout="wide")
st.title("Language Translater")

# Input language selection
st.subheader("Select Input Language")
input_language_options = list(LANGUAGES.values())
input_language = st.selectbox("Input Language", ["Auto Detect"] + input_language_options)

# Input method selection
input_method = st.radio("Input Method", ("Text", "Voice"))

if input_method == "Text":
    # Input text
    st.subheader("Enter Text")
    input_text = st.text_area("Input", "", height=150)
else:
    # Voice input
    st.subheader("Record Your Voice")
    st.info("Click the 'Start Recording' button to provide voice input.")
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Recording... Please speak.")
            try:
                audio = recognizer.listen(source, timeout=5)
                input_text = recognizer.recognize_google(audio, language='auto')
                st.success("Voice successfully converted to text:")
                st.write(input_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                input_text = ""

# Output language selection
st.subheader("Choose Output Language")
output_language_options = list(LANGUAGES.values())
output_language = st.selectbox("Output Language", ["Choose Language"] + output_language_options)

# Translate button
if st.button("Translate"):
    if output_language == "Choose Language" or not input_text.strip():
        st.warning("Please enter text and select an output language.")
    else:
        translator = Translator()
        # Determine source language code
        if input_language == "Auto Detect":
            src_language_code = "auto"
        else:
            src_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(input_language)]

        # Find the language code for the selected output language
        dest_language_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(output_language)]

        try:
            translated = translator.translate(text=input_text, src=src_language_code, dest=dest_language_code)
            st.subheader("Output")
            st.text_area("Translated Text", translated.text, height=150, disabled=True)

            # Convert translated text to speech
            tts = gTTS(text=translated.text, lang=dest_language_code)
            tts.save("output.mp3")
            st.audio("output.mp3", format="audio/mp3", start_time=0)
        except Exception as e:
            st.error(f"An error occurred: {e}")
