from flask import Flask, render_template, jsonify
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import threading
import time
from Transcribe import transcribe
from bible_parser import parse_reference
from bible_db import get_verse

app = Flask(__name__)

current_verse = {"reference": "", "text": "", "book": "", "chapter": 0, "verse": 0}
is_listening = False

SAMPLE_RATE = 16000
DURATION = 5  # seconds per audio chunk

def listen_loop():
    global is_listening, current_verse
    while is_listening:
        # Record audio chunk
        audio = sd.rec(int(DURATION * SAMPLE_RATE),
                      samplerate=SAMPLE_RATE,
                      channels=1, dtype='int16')
        sd.wait()
        wav.write("temp_audio.wav", SAMPLE_RATE, audio)

        # Transcribe
        text = transcribe("temp_audio.wav")
        print(f"Heard: {text}")

        # Parse Bible reference
        ref = parse_reference(text)
        if ref:
            verse_text = get_verse(ref["book"], ref["chapter"], ref["verse"])
            current_verse = {
                "reference": f"{ref['book']} {ref['chapter']}:{ref['verse']}",
                "text": verse_text,
                "book": ref["book"],
                "chapter": ref["chapter"],
                "verse": ref["verse"]
            }
            print(f"Detected: {current_verse['reference']}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display")
def display():
    return render_template("display.html")

@app.route("/start")
def start():
    global is_listening
    if not is_listening:
        is_listening = True
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
    return jsonify({"status": "listening"})

@app.route("/stop")
def stop():
    global is_listening
    is_listening = False
    return jsonify({"status": "stopped"})

@app.route("/verse")
def verse():
    return jsonify(current_verse)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)