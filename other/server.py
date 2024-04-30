# # whisper_server.py
# import litserve as ls
# import whisper

# class WhisperLitAPI(ls.LitAPI):
#     def setup(self, device):
#         # Load the OpenAI Whisper model. You can specify other models like "base", "small", etc.
#         self.model = whisper.load_model("large", device='cuda')
    
#     def decode_request(self, request):
#         # Assuming the request sends the path to the audio file
#         # In a more robust implementation, you would handle audio data directly.
#         return request["audio_path"]
    
#     def predict(self, audio_path):
#         # Process the audio file and return the transcription result
#         result = self.model.transcribe(audio_path)
#         return result
    
#     def encode_response(self, output):
#         # Return the transcription text
#         return {"transcription": output["text"]}

# if __name__ == "__main__":
#     api = WhisperLitAPI()
#     server = ls.LitServer(api, accelerator="gpu", timeout=1000, workers_per_device=2)
#     server.run(port=8000)
    
    
# import whisper

# # model = whisper.load_model("large")
# model = whisper.load_model("base")
# result = model.transcribe("samples/welcome.mp3")
# print(result["text"])

# from gtts import gTTS
# import os

# text = "Load the OpenAI Whisper model. You can specify other models like base, small, etc."
# tts = gTTS(text=text, lang='en')
# tts.save("output.mp3")

# # Play the converted file
# # os.system("start output.mp3")  # For Windows
# os.system("afplay output.mp3")  # For MacOS
# # os.system("mpg321 output.mp3")  # For Linux



# import boto3
# import os

# # Create a Polly client
# polly_client = boto3.client('polly')


# # Member must satisfy enum value set: [Lotte, Maxim, Ayanda, Salli, Ola, Arthur, Ida, Tomoko, Remi, Geraint, Miguel, Elin, Lisa, Giorgio, Marlene, Ines, Kajal, Zhiyu, Zeina, Suvi, Karl, Gwyneth, Joanna, Lucia, Cristiano, Astrid, Andres, 
# # Vicki, Mia, Vitoria, Bianca, Chantal, Raveena, Daniel, Amy, Liam, Ruth, Kevin, Brian, Russell, Aria, Matthew, Aditi, Zayd, Dora, Enrique, Hans, Danielle, Hiujin, Carmen, Sofie, Gregory, 
# # Ivy, Ewa, Maja, Gabrielle, Nicole, Filiz, Camila, Jacek, Thiago, Justin, Celine, Kazuha, Kendra, Arlet, Ricardo, Mads, Hannah, Mathieu, Lea, Sergio, Hala, Tatyana, Penelope, Naja, Olivia, 
# # Ruben, Laura, Takumi, Mizuki, Carla, Conchita, Jan, Kimberly, Liv, Adriano, Lupe, Joey, Pedro, Seoyeon, Emma, Niamh, Stephen]


# response = polly_client.synthesize_speech(
#     VoiceId='Joanna',
#     OutputFormat='mp3', 
#     Text = 'Load the OpenAI Whisper model. You can specify other models like base, small, etc.?')

# # Save the audio
# file = open('output.mp3', 'wb')
# file.write(response['AudioStream'].read())
# file.close()


# os.system("afplay output.mp3")  # For MacOS



import torch
import os
from scipy.io.wavfile import write
# from IPython.display import Audio

# Install necessary Python libraries (This should be done in your system shell or use !pip in a Jupyter notebook)
# !pip install numpy scipy librosa unidecode inflect

# Assume system dependencies like libsndfile1 are already installed

device = 'cuda'
# Load pre-trained Tacotron2 model

tacotron2 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tacotron2', model_math='fp16')
tacotron2 = tacotron2.to(device)
tacotron2.eval()

# Load pre-trained WaveGlow model
waveglow = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_waveglow', model_math='fp16')
waveglow = waveglow.remove_weightnorm(waveglow)
waveglow = waveglow.to(device)
waveglow.eval()

# Prepare the input text
text = "Hello world, I missed you so much."
utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')
sequences, lengths = utils.prepare_input_sequence([text])

# Generate speech
with torch.no_grad():
    mel, _, _ = tacotron2.infer(sequences, lengths)
    audio = waveglow.infer(mel)
audio_numpy = audio[0].data.cpu().numpy()
rate = 22050

# Write to a file
write("audio.wav", rate, audio_numpy)

os.system("afplay audio.wav")  # For MacOS

# Play it directly in a Jupyter Notebook
# Audio(audio_numpy, rate=rate)
