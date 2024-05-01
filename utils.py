


import boto3
from pathlib import Path
import torch
from scipy.io.wavfile import write
import whisper
from gtts import gTTS
import io
import soundfile as sf


class Whisper():
    """
    Speech to text conversion using OpenAI's Whisper model.
    """
    def generate(self, voice_path):
        # model = whisper.load_model("large")
        model = whisper.load_model("base")
        result = model.transcribe(voice_path)
        return result["text"]


class Polly():
    """AWS Polly class for text-to-speech conversion."""
    def __init__(self):
        # Create a Polly client
        self.client = boto3.client('polly', region_name='us-west-1')
        self.text_response = []
        self.voice_files = []
        self.player = None
        
        
    def generate(self, text, file_output=None):
        # Member must satisfy enum value set: [Lotte, Maxim, Ayanda, Salli, Ola, Arthur, Ida, Tomoko, Remi, Geraint, Miguel, Elin, Lisa, Giorgio, Marlene, Ines, Kajal, Zhiyu, Zeina, Suvi, Karl, Gwyneth, Joanna, Lucia, Cristiano, Astrid, Andres, 
        # Vicki, Mia, Vitoria, Bianca, Chantal, Raveena, Daniel, Amy, Liam, Ruth, Kevin, Brian, Russell, Aria, Matthew, Aditi, Zayd, Dora, Enrique, Hans, Danielle, Hiujin, Carmen, Sofie, Gregory, 
        # Ivy, Ewa, Maja, Gabrielle, Nicole, Filiz, Camila, Jacek, Thiago, Justin, Celine, Kazuha, Kendra, Arlet, Ricardo, Mads, Hannah, Mathieu, Lea, Sergio, Hala, Tatyana, Penelope, Naja, Olivia, 
        # Ruben, Laura, Takumi, Mizuki, Carla, Conchita, Jan, Kimberly, Liv, Adriano, Lupe, Joey, Pedro, Seoyeon, Emma, Niamh, Stephen]

        self.text_response.append(text)

        if not file_output:
            file_output = f"temp_output.wav"
        
        with open(file_output, 'wb') as f:
            f.write(
                self.client.synthesize_speech(
                    VoiceId='Joanna',
                    OutputFormat='wav', 
                    Text = text)['AudioStream'].read()
                )
            self.voice_files.append(file_output)
            self.last_filename = file_output
            

class Tacotron():
    """
    Text to speech conversion using Tacotron2 and WaveGlow models. Works only on GPU.
    """
    
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
        write("tacotron.wav", rate, audio_numpy)


class GoogleTTS():
    def generate(self, text):
        
        tts = gTTS(text=text, lang='en')
        tts.save("google.mp3")
        

# Assuming `audio_bytes` is your audio file in bytes
def write_to_temp_audio(audio_bytes, output_path='temp_input.wav'):
    # Convert bytes to a WAV file format in a buffer
    with io.BytesIO(audio_bytes) as audio_buffer:
        # Read the audio buffer with soundfile
        data, samplerate = sf.read(audio_buffer)
        
        # Save to a temporary WAV file
        temp_file_path = output_path
        sf.write(temp_file_path, data, samplerate)
