import pyaudio, wave, tempfile, os, threading, struct, time

CHUNK    = 1024
FORMAT   = pyaudio.paInt16
CHANNELS = 1
RATE     = 16000

SILENCE_THRESHOLD    = 600
SPEECH_MIN_CHUNKS    = 8
SILENCE_AFTER_SPEECH = 0.8
MAX_SEGMENT_SECONDS  = 10

def rms(data):
    count = len(data) // 2
    if count == 0: return 0
    shorts = struct.unpack('%dh' % count, data)
    return (sum(s*s for s in shorts) / count) ** 0.5

def save_wav(frames, p):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    return tmp.name

def cleanup_audio(filepath):
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass

def continuous_listen(on_segment, stop_event):
    """
    Runs for the full church service (2-3 hrs).
    Mic never pauses — transcription runs in parallel daemon threads.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    print("[Listener] ✓ Mic is live — listening for full service...")

    silence_chunks_needed = int(RATE / CHUNK * SILENCE_AFTER_SPEECH)
    max_chunks            = int(RATE / CHUNK * MAX_SEGMENT_SECONDS)
    frames = []; silent_chunks = 0; speech_chunks = 0; in_speech = False

    try:
        while not stop_event.is_set():
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
            except Exception as e:
                print(f"[Listener] Read error: {e}")
                time.sleep(0.05)
                continue

            loud = rms(data) > SILENCE_THRESHOLD
            if loud:
                if not in_speech:
                    in_speech = True; silent_chunks = 0
                    print("[Listener] Speech detected...")
                speech_chunks += 1; silent_chunks = 0
                frames.append(data)
            else:
                if in_speech:
                    silent_chunks += 1
                    frames.append(data)
                    if silent_chunks >= silence_chunks_needed or len(frames) >= max_chunks:
                        if speech_chunks >= SPEECH_MIN_CHUNKS:
                            fp = save_wav(frames, p)
                            print(f"[Listener] Segment ready ({round(speech_chunks*CHUNK/RATE,1)}s)")
                            threading.Thread(target=on_segment, args=(fp,), daemon=True).start()
                        else:
                            print(f"[Listener] Too short — skipping noise.")
                        frames=[]; silent_chunks=0; speech_chunks=0; in_speech=False
    finally:
        stream.stop_stream(); stream.close(); p.terminate()
        print("[Listener] Mic closed.")