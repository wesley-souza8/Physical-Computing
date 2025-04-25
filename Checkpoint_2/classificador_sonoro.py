import mediapipe as mp
import numpy as np
import sounddevice as sd
import time
import os
import urllib.request
from pydub import AudioSegment
from scipy.io import wavfile

# === CONFIG ===
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/audio_classifier/yamnet/float32/1/yamnet.tflite"
MODEL_PATH = "models/yamnet.tflite"

def baixar_modelo():
    os.makedirs("models", exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        print("📥 Baixando modelo yamnet.tflite...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("✅ Modelo baixado!")
    else:
        print("✔ Modelo já está presente.")

baixar_modelo()

# === CONFIG MEDIA PIPE ===
BaseOptions = mp.tasks.BaseOptions
AudioClassifier = mp.tasks.audio.AudioClassifier  # Corrigido o caminho
AudioClassifierOptions = mp.tasks.audio.AudioClassifierOptions
AudioClassifierResult = mp.tasks.audio.AudioClassifierResult
AudioRunningMode = mp.tasks.audio.RunningMode  # Corrigido o caminho

def processar_audio(audio_data, fs, classifier, timestamp_ms):
    audio_np = np.array(audio_data, dtype=np.float32).flatten()
    classifier.classify_async(audio_np, timestamp_ms)

def detectar_microfone(duration=10):
    print("🎤 Escutando pelo microfone...")

    options = AudioClassifierOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=AudioRunningMode.LIVE_STREAM,
        result_callback=print_result
    )
    classifier = AudioClassifier.create_from_options(options)

    fs = 16000
    start_time = time.time()
    while time.time() - start_time < duration:
        audio = sd.rec(int(0.975 * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        timestamp = int((time.time() - start_time) * 1000)
        processar_audio(audio, fs, classifier, timestamp)

def detectar_audio_mp3(nome_arquivo):
    caminho_arquivo = f"assets/audio/{nome_arquivo}"
    print(f"🔊 Processando áudio: {caminho_arquivo}")
    audio = AudioSegment.from_file(caminho_arquivo)
    audio = audio.set_channels(1).set_frame_rate(16000)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")

    fs, audio_np = wavfile.read(wav_path)

    options = AudioClassifierOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=AudioRunningMode.AUDIO_CLIPS
    )
    classifier = AudioClassifier.create_from_options(options)
    result = classifier.classify(audio_np)
    for classification in result.classifications:
        for category in classification.categories[:5]:
            print(f"🔎 {category.category_name} ({category.score:.2f})")

def detectar_video(nome_arquivo):
    caminho_video = f"assets/video/{nome_arquivo}"
    print(f"🎬 Processando vídeo: {caminho_video}")
    audio = AudioSegment.from_file(caminho_video)
    audio = audio.set_channels(1).set_frame_rate(16000)
    wav_path = "temp_video_audio.wav"
    audio.export(wav_path, format="wav")

    fs, audio_np = wavfile.read(wav_path)

    options = AudioClassifierOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=AudioRunningMode.AUDIO_CLIPS
    )
    classifier = AudioClassifier.create_from_options(options)
    result = classifier.classify(audio_np)
    for classification in result.classifications:
        for category in classification.categories[:5]:
            print(f"🔎 {category.category_name} ({category.score:.2f})")

def print_result(result: AudioClassifierResult, timestamp_ms: int):
    if result.classifications:
        top = result.classifications[0].categories[0]
        print(f"[{timestamp_ms}ms] SOM DETECTADO: {top.category_name} - Score: {top.score:.2f}")

# === EXECUÇÃO PRINCIPAL ===
print("\nEscolha a fonte de áudio:")
print("1 - Microfone")
print("2 - Áudio MP3 (coloque em assets/audio/)")
print("3 - Vídeo MP4 (coloque em assets/video/)")
opcao = input("Digite o número: ")

if opcao == '1':
    detectar_microfone()
elif opcao == '2':
    nome_arquivo = input("Digite o nome do arquivo .mp3 (ex: teste.mp3): ")
    detectar_audio_mp3(nome_arquivo)
elif opcao == '3':
    nome_arquivo = input("Digite o nome do arquivo .mp4 (ex: teste.mp4): ")
    detectar_video(nome_arquivo)
else:
    print("❌ Opção inválida.")