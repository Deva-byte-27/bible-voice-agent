from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading, time

from search import get_verse
from parser import parse_reference
from display import show_verse
from speech import smart_transcribe, detect_language

app = Flask(__name__)
CORS(app)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-store"
    return r

# ─────────────────────────────────────────
# Preacher controls — changeable at any time
# display_mode:    'tamil' | 'english' | 'both'
# english_version: 'kjv'   | 'niv'    | 'esv' | 'nkjv'
# ─────────────────────────────────────────
display_mode    = "both"
english_version = "kjv"

state = {
    "verse":           None,
    "raw_text":        "",
    "session_active":  False,
    "status":          "idle",
    "version":         0,
    "error":           "",
    "display_mode":    "both",
    "english_version": "kjv",
}
state_lock         = threading.Lock()
session_stop_event = threading.Event()
session_thread     = None
last_reference     = None


def update_state(**kwargs):
    with state_lock:
        state.update(kwargs)
        state["version"] += 1


# ─────────────────────────────────────────
# Core: process each audio segment
# ─────────────────────────────────────────
def process_segment(audio_filepath):
    global last_reference
    from live_speech import cleanup_audio
    try:
        update_state(status="processing")
        result = smart_transcribe(audio_filepath)
        text   = result.get("text","").strip()
        if not text:
            update_state(status="listening"); return

        lang = "tamil" if result.get("language") == "ta" else "english"
        print(f"[Process] ({lang}): '{text}'")
        update_state(raw_text=f"{text} ({lang})", status="listening")

        book_code, chapter, verse = parse_reference(text)
        if not book_code or not chapter or not verse:
            print(f"[Process] No reference in: '{text}'"); return

        ref_key = f"{book_code}.{chapter}.{verse}"
        if ref_key == last_reference:
            print(f"[Process] Duplicate, skip: {ref_key}"); return

        verse_data = get_verse(book_code, chapter, verse,
                               display_mode=display_mode,
                               english_version=english_version)
        payload    = show_verse(verse_data)
        update_state(verse=payload, status="listening")
        last_reference = ref_key
        print(f"[Process] ✓ {payload['reference']}")

    except Exception as e:
        print(f"[Process ERROR] {e}")
        update_state(error=str(e), status="listening")
    finally:
        cleanup_audio(audio_filepath)


# ─────────────────────────────────────────
# Session
# ─────────────────────────────────────────
def run_session():
    from live_speech import continuous_listen
    try:
        continuous_listen(on_segment=process_segment, stop_event=session_stop_event)
    except Exception as e:
        print(f"[Session ERROR] {e}")
    finally:
        update_state(session_active=False, status="idle")

def start_session():
    global session_thread, last_reference
    with state_lock:
        if state["session_active"]: return False
        state.update(session_active=True, status="listening")
        state["version"] += 1
    session_stop_event.clear()
    last_reference = None
    session_thread = threading.Thread(target=run_session, daemon=True)
    session_thread.start()
    print("[Session] Started — listening for full service.")
    return True

def stop_session():
    session_stop_event.set()
    update_state(session_active=False, status="idle")


# ─────────────────────────────────────────
# Routes
# ─────────────────────────────────────────
@app.route("/")
def index(): return render_template("index.html")

@app.route("/display")
def display_page(): return render_template("display.html")

@app.route("/api/poll")
def api_poll():
    client_v = int(request.args.get("version", 0))
    deadline = time.time() + 20
    while time.time() < deadline:
        with state_lock:
            if state["version"] > client_v:
                return jsonify({**state, "ok": True})
        time.sleep(0.2)
    with state_lock:
        return jsonify({**state, "ok": True})

@app.route("/api/state")
def api_state():
    with state_lock: return jsonify({**state, "ok": True})

@app.route("/api/start", methods=["POST"])
def api_start():
    start_session()
    with state_lock: return jsonify({**state, "ok": True})

@app.route("/api/stop", methods=["POST"])
def api_stop():
    stop_session()
    with state_lock: return jsonify({**state, "ok": True})

@app.route("/api/clear", methods=["POST"])
def api_clear():
    global last_reference
    last_reference = None
    update_state(verse=None, raw_text="", error="")
    with state_lock: return jsonify({**state, "ok": True})

@app.route("/api/settings", methods=["POST"])
def api_settings():
    """
    Preacher control: set display_mode and/or english_version.
    Body: { "display_mode": "tamil"|"english"|"both",
            "english_version": "kjv"|"niv"|"esv"|"nkjv" }
    Takes effect on the NEXT detected verse.
    """
    global display_mode, english_version
    data = request.get_json()

    if "display_mode" in data:
        display_mode = data["display_mode"]
        print(f"[Settings] display_mode → {display_mode}")

    if "english_version" in data:
        english_version = data["english_version"]
        print(f"[Settings] english_version → {english_version}")

    update_state(display_mode=display_mode, english_version=english_version)
    with state_lock: return jsonify({**state, "ok": True})

@app.route("/api/settings", methods=["GET"])
def api_get_settings():
    return jsonify({"ok": True, "display_mode": display_mode,
                    "english_version": english_version})

@app.route("/api/manual", methods=["POST"])
def api_manual():
    global last_reference
    data = request.get_json()
    text = data.get("text","").strip()
    if not text: return jsonify({"ok": False, "error": "No text"})

    book_code, chapter, verse = parse_reference(text)
    if not book_code or not chapter or not verse:
        return jsonify({"ok": False, "error": f"Cannot parse: '{text}'"})

    verse_data = get_verse(book_code, chapter, verse,
                           display_mode=display_mode,
                           english_version=english_version)
    payload    = show_verse(verse_data)
    last_reference = f"{book_code}.{chapter}.{verse}"
    update_state(verse=payload, error="")
    with state_lock: return jsonify({**state, "ok": True})


# ─────────────────────────────────────────
# Run
# ─────────────────────────────────────────
if __name__ == "__main__":
    import socket as _s
    try:
        s = _s.socket(_s.AF_INET, _s.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close()
    except: ip = "127.0.0.1"

    print("\n" + "="*60)
    print("   ✝  BIBLE SPEECH RECOGNITION  ✝")
    print("="*60)
    print(f"   Preacher Control  →  http://localhost:5000")
    print(f"   TV / Phone Screen →  http://{ip}:5000/display")
    print(f"   Same WiFi required for all devices")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)