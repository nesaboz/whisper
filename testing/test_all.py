import os
from utils import Polly, Whisper

from openai import OpenAI, RateLimitError


def test_llm_client():
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))   
    
    chat = [{'role': 'system', 'content': "You are helpful assistant."}, {'role': 'user', 'content': "what's 2+2"}]
    
    reply = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat,
        max_tokens=500
        )

    answer = reply.choices[0].message.content
    
    

def test_polly():
    POLLY = Polly()
    test_filename = "testing/test.mp3"
    POLLY.generate("pera, zika, mika", test_filename)
    POLLY.talk()
    assert os.path.exists(test_filename)
    try:
        os.remove(test_filename)
    except OSError as e:
        print(f"Error: {test_filename} : {e.strerror}")
    
    
def test_whisper():
    assert "Okay, how are you doing?" == Whisper().generate('testing/test_whisper.wav').strip()
    
    
def test_text_to_speech():
    text = "Hello, great to see you again here, and good luck!"
    
    # outputs = Path('outputs')
    # outputs.mkdir(parents=True, exist_ok=True)
        
    # Polly().generate(text)
    # Tacotron().generate(text)
    # GoogleTTS().generate(text)
    
    # print(Whisper().generate(outputs/"google.mp3"))
    
    # os.system("afplay audio.wav")  # For MacOS
    # os.system("mpg321 audio.wav")  # For Linux
    # Audio(audio_numpy, rate=rate)  # Play it directly in a Jupyter Notebook
