""" 
https://github.com/thewh1teagle/kokoro-onnx/blob/main/examples/with_gpu.py

Note:
    On Linux you need to run this as well: apt-get install portaudio19-dev
    gpu version is sufficient only for Linux and Windows. macOS works with GPU by default.
    You can see the used execution provider by enable debug log. see with_log.py

Setup:
    pip install kokoro-onnx[gpu] sounddevice
    wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx
    wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin

Run:
python examples/play.py
"""

from kokoro_onnx import Kokoro
from fastapi import FastAPI
import uvicorn
from base64 import b64encode

app = FastAPI()
kokoro = Kokoro("./kokoro_server/kokoro-v0_19.onnx", "./kokoro_server/voices.bin")


@app.get("/get_snd")
def read_root(text: str):
    samples, sample_rate = kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")
    enc = b64encode(samples)
    print(f"sample rate {sample_rate}")
    return enc

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(8863))
    






# from openai import OpenAI
# client = OpenAI(
#     base_url="http://localhost:8880/v1",
#     api_key="not-needed"
#     )

# with client.audio.speech.with_streaming_response.create(
#     model="kokoro", 
#     voice="af_sky+af_bella", #single or multiple voicepack combo
#     input="Hello world!",
#     response_format="mp3"
# ) as response:
#     response.stream_to_file("output.mp3")
