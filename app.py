import streamlit as st

from ai_engine import ask_ai
from emergency import detect_emergency
from database import save_data

st.set_page_config(
    page_title="Healthcare AI Assistant",
    layout="centered"
)a

st.title("Voice AI Healthcare Assistant")
st.write("AI healthcare companion for elderly patients")

# Sidebar
st.sidebar.title("Patient Details")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", 1, 120)

st.divider()

# ---------------- INPUT OPTIONS ----------------
st.subheader("Input Method")

input_mode = st.radio("Choose input type:", ["Type Text", "Upload Audio"])

user_text = ""

# TEXT INPUT
if input_mode == "Type Text":
    user_text = st.text_area("Enter patient message")

# AUDIO INPUT (SAFE for Streamlit)
else:
    audio_file = st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"])

    if audio_file is not None:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        audio = sr.AudioFile(audio_file)

        with audio as source:
            data = recognizer.record(source)

        try:
            user_text = recognizer.recognize_google(data)
            st.success("Transcribed Text:")
            st.write(user_text)
        except Exception as e:
            st.error(f"Could not understand audio: {e}")

# ---------------- MAIN LOGIC ----------------
if st.button("Process") and user_text:

    emergency = detect_emergency(user_text)

    if emergency:
        alert = """
🚨 Emergency detected.
Please contact doctor immediately.
"""
        st.error(alert)

    else:
        response = ask_ai(user_text)
        st.success(response)

        save_data(user_text, response)
