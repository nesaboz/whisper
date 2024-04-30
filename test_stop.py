import streamlit as st
from audio_recorder_streamlit import audio_recorder
from main import Polly

ss = st.session_state

if 'first time' not in st.session_state:
    ss['first time'] = False
    ss['talker'] = Polly()

ss['talker'].last_filename = 'testing/test_whisper.wav'

# talker.play_audio()
import subprocess
import time


# Function to play audio
def play_audio(filename):
    # Start the audio playback
    ss['player'] = subprocess.Popen(["afplay", filename])

# Function to stop audio
def stop_audio():
    # Stop the audio playback
    ss['player'].terminate()


filename = 'testing/test_whisper.wav'
    
st.button("Play", key='play', on_click=play_audio, args=(filename, ))

st.button("Stop", key='stop', on_click=stop_audio)

