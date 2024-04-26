


import boto3
import os
from pathlib import Path
import torch
from scipy.io.wavfile import write
from gtts import gTTS
import whisper




class Polly():
    def __init__(self):
        # Create a Polly client
        self.client = boto3.client('polly')
        self.response = []
        
    def generate(self, text):
        # Member must satisfy enum value set: [Lotte, Maxim, Ayanda, Salli, Ola, Arthur, Ida, Tomoko, Remi, Geraint, Miguel, Elin, Lisa, Giorgio, Marlene, Ines, Kajal, Zhiyu, Zeina, Suvi, Karl, Gwyneth, Joanna, Lucia, Cristiano, Astrid, Andres, 
        # Vicki, Mia, Vitoria, Bianca, Chantal, Raveena, Daniel, Amy, Liam, Ruth, Kevin, Brian, Russell, Aria, Matthew, Aditi, Zayd, Dora, Enrique, Hans, Danielle, Hiujin, Carmen, Sofie, Gregory, 
        # Ivy, Ewa, Maja, Gabrielle, Nicole, Filiz, Camila, Jacek, Thiago, Justin, Celine, Kazuha, Kendra, Arlet, Ricardo, Mads, Hannah, Mathieu, Lea, Sergio, Hala, Tatyana, Penelope, Naja, Olivia, 
        # Ruben, Laura, Takumi, Mizuki, Carla, Conchita, Jan, Kimberly, Liv, Adriano, Lupe, Joey, Pedro, Seoyeon, Emma, Niamh, Stephen]

        self.response.append(self.client.synthesize_speech(
            VoiceId='Joanna',
            OutputFormat='mp3', 
            Text = text))
        
        with open(outputs/'polly.mp3', 'wb') as f:
            f.write(self.response[-1]['AudioStream'].read())
        
        

class Tacotron():
    
    def __init__(self):
        
        # from IPython.display import Audio

        # Install necessary Python libraries (This should be done in your system shell or use !pip in a Jupyter notebook)
        # !pip install numpy scipy librosa unidecode inflect

        # Assume system dependencies like libsndfile1 are already installed

        device = 'cuda'
        # Load pre-trained Tacotron2 model

        tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', model_math='fp16')
        tacotron2 = tacotron2.to(device)
        tacotron2.eval()
        
        self.tacotron2 = tacotron2

        # Load pre-trained WaveGlow model
        waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', model_math='fp16')
        waveglow = waveglow.remove_weightnorm(waveglow)
        waveglow = waveglow.to(device)
        waveglow.eval()
        
        self.waveglow = waveglow
        
        self.utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')
        

    def generate(self, text):
        
        sequences, lengths = self.utils.prepare_input_sequence([text])

        # Generate speech
        with torch.no_grad():
            mel, _, _ = self.tacotron2.infer(sequences, lengths)
            audio = self.waveglow.infer(mel)
        audio_numpy = audio[0].data.cpu().numpy()
        rate = 22050

        # Write to a file
        write(outputs/"tacotron.wav", rate, audio_numpy)


class GoogleTTS():
    def generate(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save(outputs/"google.mp3")
        
        
class Whisper():
    def generate(self, voice_path):
        # model = whisper.load_model("large")
        model = whisper.load_model("base")
        result = model.transcribe(voice_path)
        return result["text"]


if __name__ == "__main__":

    text = "Hello, great to see you again here, and good luck!"
    outputs = Path('outputs')
    outputs.mkdir(parents=True, exist_ok=True)
        

    # polly = Polly()
    # polly.generate(text)
    
    # tacotron = Tacotron()
    # tacotron.generate(text)
    
    # GoogleTTS().generate(text)
    
    whisper = Whisper()
    print(whisper.generate(outputs/"google.mp3"))
    
    

    # os.system("afplay audio.wav")  # For MacOS
    # os.system("mpg321 audio.wav")  # For Linux
    # Audio(audio_numpy, rate=rate)  # Play it directly in a Jupyter Notebook
