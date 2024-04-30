
"""
The key variable below st.session_state['chat'], which is list of dictionaries with keys 'role' and 'content'. 
First item is system role, then 2N pairs of questions and answers.
"""

import streamlit as st
import os
from openai import OpenAI
from utils import Polly, Whisper
from utils import write_to_temp_audio
from audio_recorder_streamlit import audio_recorder
from typing import List
import subprocess


# Custom CSS to inject for making buttons bigger
css = """
<style>
.stButton>button {
    background-image: url('http://www.clker.com/cliparts/5/A/k/D/X/A/stop-button-md.png');
    width: 150px !important;
    height: 150px !important;
    background-size: cover; /* Cover the entire area of the button */
    border: none;
}
</style>
"""

# Inject custom CSS with markdown
st.markdown(css, unsafe_allow_html=True)


ss = st.session_state 


# Function to send requests to your GPT model
def send_message(llm_client: OpenAI, question: str, old_chat: List[dict]):
    """
    Calls OpenAI API, if error occurs, reverts back to the old chat history and leave the question in the text input.
    """
    try:
        # stores new chat, removes the old input
        new_chat = old_chat.copy()
        new_chat.append({'role': 'user', 'content': question})
        
        reply = llm_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=new_chat,
            max_tokens=500
            )

        answer = reply.choices[0].message.content
        new_chat.append({'role': 'assistant', 'content': answer})
        
        user_input = ''
        error = None
        
    except Exception as e:
        # will have to show the same chat old again and will leave old input as is
        new_chat = old_chat
        user_input = question
        error = e
        
    return new_chat, user_input, error


def stop_audio():
    ss['player'].terminate()
    ss['stopped'] = True
    

if __name__ == "__main__":

    st.title("Ella App v0.1")

    st.info(f"""
            Welcome to Ella App, an AI therapist. Works only in Chrome.
    """)

    if 'first time' not in st.session_state:
        ss['input_text'] = ''
        ss['error'] = None
        ss['chat'] = []
        ss['first time'] = False
        
        ss['whisper'] = Whisper()
        ss['polly'] = Polly()
        
        ss['stopped'] = False

        ss['user_input'] = None
        ss['llm_client'] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   

        # assign role:
        ss['chat'].append({'role': 'system', 'content': """You are AI therapist who primarily
                           responds with brief, question-driven dialogue, encouraging users to   
                           explore their feelings and thoughts. You provide brief suggestions
                           and ask probing questions to facilitate self-reflection,
                           only elaborating in detail when explicitly requested by the user.
                           This approach helps maintain an engaging and reflective conversation,
                           guiding users towards self-discovery and emotional awareness."""})
        
        # ss['chat'].append({'role': 'system', 'content': """You are expert machine learning engineer
        #                   give me only very short answers and directly in Python or Bash code depending on the context. I will ask you if I need more details."""})
        

    col1, col2 = st.columns(2)

    with col1:
        ss['audio_bytes'] = audio_recorder(text='', icon_size='10x', pause_threshold=30)

    with col2:
        st.button(" ", key='stop', on_click=stop_audio)

    # crux of the code, get user input and send it to OpenAI
    if ss['audio_bytes'] and not ss['stopped']:
        # this will save the audio to a file temp_audio.wav
        write_to_temp_audio(ss['audio_bytes'], 'temp_audio.wav')
        
        # this optionally shows the audio bar
        # st.audio(ss['audio_bytes'], format="audio/wav")
        
        # this will convert the audio to text
        user_input_txt = ss['whisper'].generate('temp_audio.wav')
        
        # this will send the text to OpenAI
        ss['user_input'] = user_input_txt
        ss['chat'], ss['user_input'], ss['error'] = send_message(ss['llm_client'], ss['user_input'], ss['chat'])
        
        # this will write the answer to a mp3 file
        ss['polly'].generate(ss['chat'][-1]['content'])
        
        # this will start playing the mp3 file
        ss['player'] = subprocess.Popen(["afplay", ss['polly'].last_filename])
    
    
    ### Show all previous Q&A
    for i in range(1, len(ss['chat']), 2):
        question = ss['chat'][i]['content']
        answer = ss['chat'][i+1]['content']
        
        st.write(question)
        st.markdown(f'<div style="color: gray;">{answer}</div>', unsafe_allow_html=True) 
        st.text("\n" * 10)
    
    ss['stopped'] = False
    
    # if ss['error'] is not None:
    #     st.error(f"API issue encountered on OpenAI side, try again ...")  
        
        
    ## DEBUGGING
    
    # "debug", ss['chat']
    # "error", ss['error']


