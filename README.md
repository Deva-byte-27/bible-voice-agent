# 📖 Bible Voice Recognition Agent

A real-time voice-powered Bible verse retrieval system. Speak a Bible reference out loud — the app listens, transcribes it, parses the reference, and instantly displays the verse.

> "Matthew chapter 22 verse 15" → displays Matthew 22:15 on screen

---

## 🎯 What It Does

| Step | What Happens |
|------|-------------|
| 🎙️ Listen | Records 5-second audio chunks from microphone |
| ✍️ Transcribe | Converts speech to text using OpenAI Whisper |
| 🔍 Parse | Extracts book, chapter, verse from natural speech |
| 📖 Retrieve | Looks up the verse from a local Bible JSON database |
| 🖥️ Display | Serves the result live via a Flask web interface |

---

## 🗣️ Supported Speech Patterns

```
"John chapter 3 verse 16"
"Matthew 22 15"
"Genesis chapter 1 verse 1"
"யோவான் 3 16"          ← Tamil
"மத்தேயு chapter 5 verse 9"  ← Tamil book name, English structure
```

Supports **English and Tamil** book names across the full Old and New Testament.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Speech-to-Text | [OpenAI Whisper](https://github.com/openai/whisper) (`base` model) |
| Audio Recording | `sounddevice` + `scipy` |
| Reference Parser | Custom regex + word-to-number converter |
| Bible Database | Local JSON (KJV) |
| Web Server | Flask |
| Language Support | English, Tamil (auto-detect) |

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/Deva-byte-27/bible-voice-agent.git
cd bible-voice-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install ffmpeg (required by Whisper)

**Windows:**
Download from https://www.gyan.dev/ffmpeg/builds/ → extract → add `bin/` folder to PATH

**Linux/Mac:**
```bash
sudo apt install ffmpeg   # Linux
brew install ffmpeg       # Mac
```

### 4. Add Bible JSON database

Download `en_kjv.json` from [thiagobodruk/bible](https://github.com/thiagobodruk/bible/tree/master/json) and save it as `bible_en.json` in the project root.

### 5. Run

```bash
python app.py
```

Open browser → `http://localhost:5000`

---

## 📁 Project Structure

```
bible-voice-agent/
│
├── app.py            # Flask server + audio recording loop
├── Transcribe.py     # Whisper STT wrapper
├── bible_parser.py   # Reference parser (regex + word numbers)
├── bible_db.py       # JSON Bible database loader
├── test.py           # Standalone mic test script
├── requirements.txt
└── templates/
    ├── index.html    # Control panel (start/stop listening)
    └── display.html  # Live verse display
```

---

## 🧠 How the Parser Works

Whisper transcribes speech as natural text:
```
"matthew chapter twenty two verse fifteen"
```

The parser handles:
- Digit numbers: `22`, `15`
- Word numbers: `"twenty two"` → `22`, `"fifteen"` → `15`
- Optional keywords: `chapter`, `verse` are noise-tolerant
- Tamil book names mapped to English canonical names
- Fuzzy prefix matching for abbreviations (`"mat"` → `Matthew`)

---

## 📋 Requirements

```
openai-whisper
torch
flask
sounddevice
scipy
numpy
```

---

## 🔮 Planned Improvements

- [ ] MCP (Model Context Protocol) integration for agent-based querying
- [ ] Groq / vLLM backend for faster inference
- [ ] Cross-reference and commentary support
- [ ] Mobile-friendly display UI
- [ ] Verse highlighting for church/presentation use

---

## 👤 Author

**Deva** — B.Tech AI & Data Science  
Pre-final year student | Coimbatore, India  
[GitHub](https://github.com/Deva-byte-27) · [LinkedIn](www.linkedin.com/in/sanjay-deva-mastery)

---

## 📄 License

MIT License — free to use and modify.
