import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils import write_to_temp_audio, Whisper

audio_bytes = audio_recorder()

if audio_bytes:
    write_to_temp_audio(audio_bytes, 'temp_audio.wav')
    st.audio(audio_bytes, format="audio/wav")
    
    text = Whisper().generate('temp_audio.wav')
    
    st.write(text)
