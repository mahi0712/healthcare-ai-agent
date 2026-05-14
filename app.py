import streamlit as st

from voice_input import listen

from ai_engine import ask_ai

from emergency import detect_emergency

from database import save_data

st.set_page_config(

    page_title="Healthcare AI Assistant",

    layout="centered"
)

st.title("Voice AI Healthcare Assistant")

st.write("AI healthcare companion for elderly patients")

st.sidebar.title("Patient Details")

name = st.sidebar.text_input("Patient Name")

age = st.sidebar.number_input("Age", 1, 120)

if st.button("Start Listening"):

    user_text = listen()

    st.success(user_text)

    emergency = detect_emergency(user_text)

    if emergency:

        alert = """

Emergency detected.
Please contact doctor immediately.

"""

        st.error(alert)

    else:

        response = ask_ai(user_text)

        st.success(response)

        save_data(user_text, response)