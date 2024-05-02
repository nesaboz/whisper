import streamlit as st
import base64

ss = st.session_state


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


# Function to play audio
def play_audio(filename):
    # Start the audio playback
    autoplay_audio("test_whisper.wav")

filename = 'test_whisper.wav'
    
st.button("Play", key='play', on_click=play_audio, args=(filename, ))
