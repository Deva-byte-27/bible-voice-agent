import whisper

_model      = None
_tiny_model = None

def get_model():
    global _model
    if _model is None:
        print("[Whisper] Loading small model...")
        _model = whisper.load_model("small")
        print("[Whisper] Small model ready.")
    return _model

def get_tiny_model():
    global _tiny_model
    if _tiny_model is None:
        print("[Whisper] Loading tiny model...")
        _tiny_model = whisper.load_model("tiny")
        print("[Whisper] Tiny model ready.")
    return _tiny_model

def _detect_audio_language(audio_file: str) -> str:
    """Fast language detection using tiny model (~0.3s)."""
    try:
        tiny  = get_tiny_model()
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel   = whisper.log_mel_spectrogram(audio).to(tiny.device)
        _, probs = tiny.detect_language(mel)
        lang = max(probs, key=probs.get)
        print(f"[LangDetect] '{lang}' ({probs.get(lang,0):.2f})")
        return lang
    except Exception as e:
        print(f"[LangDetect ERROR] {e} — defaulting to Tamil")
        return "ta"

def smart_transcribe(audio_file: str) -> dict:
    """
    Two-stage transcription:
      1. Tiny model detects language quickly  (~0.3s)
      2. Small model transcribes in that language (~1-3s)
    Mic thread is never blocked — this runs in a daemon thread.
    """
    lang_code = _detect_audio_language(audio_file)
    model = get_model()
    try:
        result = model.transcribe(audio_file, language=lang_code, task="transcribe", fp16=False)
        text = result["text"].strip()
        print(f"[Whisper/{lang_code}] → '{text}'")
        return {"text": text, "language": lang_code}
    except Exception as e:
        print(f"[Whisper ERROR] {e}")
        return {"text": "", "language": lang_code}

def detect_language(text: str) -> str:
    if any('\u0B80' <= c <= '\u0BFF' for c in text):
        return "tamil"
    return "english"