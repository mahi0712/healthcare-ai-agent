import streamlit as st
import io

import speech_recognition as sr

from ai_engine import ask_ai
from emergency import detect_emergency
from database import save_data


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Healthcare AI Assistant",
    layout="centered"
)

st.title("Voice AI Healthcare Assistant")
st.write("AI healthcare companion for elderly patients")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Patient Details")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", 1, 120)

st.divider()

# ---------------- AUDIO INPUT ----------------
st.subheader("🎤 Speak or Upload Audio")

audio_file = st.file_uploader("Upload your voice (wav format recommended)", type=["wav"])

user_text = ""

if audio_file is not None:
    recognizer = sr.Recognizer()

    audio_bytes = io.BytesIO(audio_file.read())
    audio = sr.AudioFile(audio_bytes)

    with audio as source:
        data = recognizer.record(source)

    try:
        user_text = recognizer.recognize_google(data)
        st.success("Transcribed Text:")
        st.write(user_text)

    except Exception as e:
        st.error(f"Could not understand audio: {e}")

# ---------------- PROCESS ----------------
if st.button("Process") and user_text:

    emergency = detect_emergency(user_text)

    if emergency:
        st.error("🚨 Emergency detected! Please contact a doctor immediately.")

    else:
        response = ask_ai(user_text)
        st.success("AI Response:")
        st.write(response)

        save_data(user_text, response)
