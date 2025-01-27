from models import build_model
import torch
import numpy as np
import pyaudio
import wave
import sys
import soundfile as sf
import sounddevice as sd
import simpleaudio as sa
from kokoro import generate

def stream_audio(audio, sample_rate=24000):
    wave_obj = sa.WaveObject.from_wave_file('output.wav')
    
    play_obj = wave_obj.play()
    play_obj.wait_done()

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        info.append(f"Device {i}: {device_info['name']}")
    p.terminate()
    return info

def play_audio(audio, sample_rate=24000):
    try:
        sd.play(audio, sample_rate)
        sd.wait()  # Wait until audio finishes playing
    except Exception as e:
        print(f"Error playing audio: {e}")

def stream_it(audio):
    CHUNK = 1024
    wf = wave.open('output.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True
                    )

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = [
    'af', # Default voice is a 50-50 mix of Bella & Sarah
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', 'af_sky',
][0]
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')

# 3️⃣ Call generate, which returns 24khz audio and the phonemes used

text = "reminder of the Grade 12 Literacy Assessment that will be taking place tomorrow morning and afternoon. \
    Please ensure that you/ your student knows the time and location of their assessment. Students should bring a pen and are permitted to have a water bottle. \
    Please plan to arrive to your assessment location 10 minutes before it starts in order to get setup up."
audio, out_ps = generate(MODEL, text, VOICEPACK, lang=VOICE_NAME[0])
# Language is determined by the first letter of the VOICE_NAME:
# 🇺🇸 'a' => American English => en-us
# 🇬🇧 'b' => British English => en-gb

if isinstance(audio, np.ndarray):
    audio = audio.astype(np.float32)
sf.write('output1.wav', audio, samplerate=24000)

# stream_audio(audio)

# 4️⃣ Display the 24khz audio and print the output phonemes
# from IPython.display import display, Audio
# ad = Audio(data=audio, rate=24000, autoplay=True)
# display(ad)
# print(out_ps)

ad = pyaudio.PyAudio()
stream = ad.open(format=pyaudio.paFloat32, channels=1, rate=24000, output=True)
stream.write(audio.tobytes())


