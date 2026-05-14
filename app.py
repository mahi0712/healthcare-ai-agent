import streamlit as st
import av
import numpy as np
import speech_recognition as sr

from streamlit_webrtc import webrtc_streamer, AudioProcessorBase

from ai_engine import ask_ai
from emergency import detect_emergency
from database import save_data


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Healthcare AI Assistant",
    layout="centered"
)

st.title("🎤 Voice AI Healthcare Assistant")
st.write("Speak like WhatsApp voice note")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Patient Details")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", 1, 120)

# ---------------- AUDIO PROCESSOR ----------------
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray())
        return frame


# ---------------- MIC STREAM ----------------
ctx = webrtc_streamer(
    key="voice",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

user_text = ""

# ---------------- PROCESS ----------------
if ctx.audio_processor and st.button("Process Voice"):

    try:
        audio_data = np.concatenate(ctx.audio_processor.frames, axis=1)

        recognizer = sr.Recognizer()

        audio = sr.AudioData(
            audio_data.tobytes(),
            sample_rate=48000,
            sample_width=2
        )

        user_text = recognizer.recognize_google(audio)

        st.success("You said:")
        st.write(user_text)

        # AI logic
        emergency = detect_emergency(user_text)

        if emergency:
            st.error("🚨 Emergency detected! Contact doctor immediately.")
        else:
            response = ask_ai(user_text)
            st.success(response)

            save_data(user_text, response)

    except Exception:
        st.error("Could not understand audio")
