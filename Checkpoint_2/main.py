import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

def gravar_audio(duracao=5, fs=44100, arquivo='audio.wav'):
    print("Gravando por", duracao, "segundos...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(arquivo, fs, audio)
    print("Áudio salvo como", arquivo)

def transcrever_audio(arquivo='audio.wav'):
    model = whisper.load_model("base")  # ou "tiny", "small", "medium", "large"
    result = model.transcribe(arquivo, language='pt')
    return result["text"]


gravar_audio()

frase = transcrever_audio()
print("🗣 Frase detectada:", frase)

if "hoje é dia 24" in frase.lower():
    print("✔ A frase contém 'hoje é dia 24'")
else:
    print("❌ Frase não reconhecida.")
