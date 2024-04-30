import streamlit as st
import subprocess

ss = st.session_state

# Function to play audio
def play_audio(filename):
    # Start the audio playback
    ss['player'] = subprocess.Popen(["afplay", filename])

# Function to stop audio
def stop_audio():
    # Stop the audio playback
    ss['player'].terminate()
    

if 'first time' not in st.session_state:
    ss['first time'] = False

filename = 'testing/test_whisper.wav'
    
st.button("Play", key='play', on_click=play_audio, args=(filename, ))
st.button("Stop", key='stop', on_click=stop_audio)
