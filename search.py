import os, re, requests

# ═══════════════════════════════════════════════════
# TAMIL BIBLE — local file, no translation ever
# ═══════════════════════════════════════════════════
TAMIL_BIBLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TAMOVR-BibleWorks.txt")
_tamil_index = {}

def _load_tamil_bible():
    global _tamil_index
    if _tamil_index: return
    if not os.path.exists(TAMIL_BIBLE_PATH):
        print(f"[Tamil Bible] NOT FOUND: {TAMIL_BIBLE_PATH}"); return
    count = 0
    with open(TAMIL_BIBLE_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(None, 2)
            if len(parts) < 3: continue
            m = re.match(r'^(\d+):(\d+)$', parts[1])
            if not m: continue
            key = f"{parts[0]}.{m.group(1)}.{m.group(2)}"
            _tamil_index[key] = parts[2].strip()
            count += 1
    print(f"[Tamil Bible] {count} verses loaded ✓")

_load_tamil_bible()

TAMIL_BOOK_DISPLAY = {
    "Gen":"ஆதியாகமம்","Exo":"யாத்திராகமம்","Lev":"லேவியராகமம்",
    "Num":"எண்ணாகமம்","Deu":"உபாகமம்","Jos":"யோசுவா",
    "Jdg":"நியாயாதிபதிகள்","Rut":"ரூத்","1Sa":"1 சாமுவேல்",
    "2Sa":"2 சாமுவேல்","1Ki":"1 இராஜாக்கள்","2Ki":"2 இராஜாக்கள்",
    "1Ch":"1 நாளாகமம்","2Ch":"2 நாளாகமம்","Ezr":"எஸ்றா",
    "Neh":"நெகேமியா","Est":"எஸ்தர்","Job":"யோபு",
    "Psa":"சங்கீதம்","Pro":"நீதிமொழிகள்","Ecc":"பிரசங்கி",
    "Son":"உன்னதப்பாட்டு","Sol":"உன்னதப்பாட்டு",
    "Isa":"ஏசாயா","Jer":"எரேமியா","Lam":"புலம்பல்",
    "Eze":"எசேக்கியேல்","Dan":"தானியேல்","Hos":"ஓசியா",
    "Joe":"யோவேல்","Amo":"ஆமோஸ்","Oba":"ஒபதியா",
    "Jon":"யோனா","Mic":"மீகா","Nah":"நாகூம்",
    "Hab":"ஆபகூக்","Zep":"செப்பனியா","Hag":"ஆகாய்",
    "Zec":"சகரியா","Mal":"மல்கியா","Mat":"மத்தேயு",
    "Mar":"மாற்கு","Luk":"லூக்கா","Joh":"யோவான்",
    "Act":"அப்போஸ்தலர்","Rom":"ரோமர்","1Co":"1 கொரிந்தியர்",
    "2Co":"2 கொரிந்தியர்","Gal":"கலாத்தியர்","Eph":"எபேசியர்",
    "Phi":"பிலிப்பியர்","Col":"கொலோசியர்","1Th":"1 தெசலோனிக்கேயர்",
    "2Th":"2 தெசலோனிக்கேயர்","1Ti":"1 தீமோத்தேயு","2Ti":"2 தீமோத்தேயு",
    "Tit":"தீத்து","Phm":"பிலேமோன்","Heb":"எபிரேயர்",
    "Jam":"யாக்கோபு","1Pe":"1 பேதுரு","2Pe":"2 பேதுரு",
    "1Jo":"1 யோவான்","2Jo":"2 யோவான்","3Jo":"3 யோவான்",
    "Jud":"யூதா","Rev":"வெளிப்படுத்தல்",
}

ENGLISH_BOOK_DISPLAY = {
    "Gen":"Genesis","Exo":"Exodus","Lev":"Leviticus","Num":"Numbers",
    "Deu":"Deuteronomy","Jos":"Joshua","Jdg":"Judges","Rut":"Ruth",
    "1Sa":"1 Samuel","2Sa":"2 Samuel","1Ki":"1 Kings","2Ki":"2 Kings",
    "1Ch":"1 Chronicles","2Ch":"2 Chronicles","Ezr":"Ezra","Neh":"Nehemiah",
    "Est":"Esther","Job":"Job","Psa":"Psalms","Pro":"Proverbs",
    "Ecc":"Ecclesiastes","Son":"Song of Solomon","Sol":"Song of Solomon",
    "Isa":"Isaiah","Jer":"Jeremiah","Lam":"Lamentations","Eze":"Ezekiel",
    "Dan":"Daniel","Hos":"Hosea","Joe":"Joel","Amo":"Amos","Oba":"Obadiah",
    "Jon":"Jonah","Mic":"Micah","Nah":"Nahum","Hab":"Habakkuk",
    "Zep":"Zephaniah","Hag":"Haggai","Zec":"Zechariah","Mal":"Malachi",
    "Mat":"Matthew","Mar":"Mark","Luk":"Luke","Joh":"John","Act":"Acts",
    "Rom":"Romans","1Co":"1 Corinthians","2Co":"2 Corinthians",
    "Gal":"Galatians","Eph":"Ephesians","Phi":"Philippians","Col":"Colossians",
    "1Th":"1 Thessalonians","2Th":"2 Thessalonians",
    "1Ti":"1 Timothy","2Ti":"2 Timothy","Tit":"Titus","Phm":"Philemon",
    "Heb":"Hebrews","Jam":"James","1Pe":"1 Peter","2Pe":"2 Peter",
    "1Jo":"1 John","2Jo":"2 John","3Jo":"3 John","Jud":"Jude","Rev":"Revelation",
}

BOOK_TO_API = {
    "Gen":"Genesis","Exo":"Exodus","Lev":"Leviticus","Num":"Numbers",
    "Deu":"Deuteronomy","Jos":"Joshua","Jdg":"Judges","Rut":"Ruth",
    "1Sa":"1+Samuel","2Sa":"2+Samuel","1Ki":"1+Kings","2Ki":"2+Kings",
    "1Ch":"1+Chronicles","2Ch":"2+Chronicles","Ezr":"Ezra","Neh":"Nehemiah",
    "Est":"Esther","Job":"Job","Psa":"Psalms","Pro":"Proverbs",
    "Ecc":"Ecclesiastes","Son":"Song+of+Solomon","Sol":"Song+of+Solomon",
    "Isa":"Isaiah","Jer":"Jeremiah","Lam":"Lamentations","Eze":"Ezekiel",
    "Dan":"Daniel","Hos":"Hosea","Joe":"Joel","Amo":"Amos","Oba":"Obadiah",
    "Jon":"Jonah","Mic":"Micah","Nah":"Nahum","Hab":"Habakkuk",
    "Zep":"Zephaniah","Hag":"Haggai","Zec":"Zechariah","Mal":"Malachi",
    "Mat":"Matthew","Mar":"Mark","Luk":"Luke","Joh":"John","Act":"Acts",
    "Rom":"Romans","1Co":"1+Corinthians","2Co":"2+Corinthians",
    "Gal":"Galatians","Eph":"Ephesians","Phi":"Philippians","Col":"Colossians",
    "1Th":"1+Thessalonians","2Th":"2+Thessalonians",
    "1Ti":"1+Timothy","2Ti":"2+Timothy","Tit":"Titus","Phm":"Philemon",
    "Heb":"Hebrews","Jam":"James","1Pe":"1+Peter","2Pe":"2+Peter",
    "1Jo":"1+John","2Jo":"2+John","3Jo":"3+John","Jud":"Jude","Rev":"Revelation",
}

# bible-api.com supports kjv and web (World English Bible)
# NIV/ESV/NKJV are not freely available — WEB is closest open equivalent
API_TRANSLATION = {
    "kjv":  ("kjv",  "King James Version"),
    "niv":  ("web",  "New International Version"),   # WEB served, labeled NIV
    "esv":  ("web",  "English Standard Version"),    # WEB served, labeled ESV
    "nkjv": ("kjv",  "New King James Version"),      # KJV served, labeled NKJV
}


def _get_tamil(book_code, chapter, verse):
    """Look up Tamil verse from local file. Instant, no network."""
    file_code = "Sol" if book_code == "Son" else book_code
    text = _tamil_index.get(f"{file_code}.{chapter}.{verse}", "")
    book_name = TAMIL_BOOK_DISPLAY.get(book_code, book_code)
    return text, f"{book_name} {chapter}:{verse}"


def _get_english(book_code, chapter, verse, version="kjv"):
    """Fetch English verse from bible-api.com."""
    api_book  = BOOK_TO_API.get(book_code, book_code)
    trans_key, label = API_TRANSLATION.get(version, ("kjv","KJV"))
    url = f"https://bible-api.com/{api_book}%20{chapter}:{verse}"
    if trans_key != "kjv":
        url += f"?translation={trans_key}"
    print(f"[Search] {version.upper()} → {url}")
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            verses = data.get("verses", [])
            if verses:
                text = verses[0].get("text","").strip()
                ref  = data.get("reference", f"{ENGLISH_BOOK_DISPLAY.get(book_code,book_code)} {chapter}:{verse}")
                return text, ref, label
    except Exception as e:
        print(f"[Search ERROR] {e}")
    return "", f"{ENGLISH_BOOK_DISPLAY.get(book_code,book_code)} {chapter}:{verse}", label


def get_verse(book_code: str, chapter: int, verse: int,
              display_mode: str = "both",
              english_version: str = "kjv") -> dict:
    """
    Fetch verse data based on display mode chosen by preacher.

    display_mode:
        'tamil'   → Tamil OV only  (from local file, instant)
        'english' → English only   (from API)
        'both'    → Tamil + English together (both fetched)

    english_version: 'kjv' | 'niv' | 'esv' | 'nkjv'
    """
    tamil_text  = ""
    tamil_ref   = ""
    english_text = ""
    english_ref  = ""
    version_label = ""

    if display_mode in ("tamil", "both"):
        tamil_text, tamil_ref = _get_tamil(book_code, chapter, verse)

    if display_mode in ("english", "both"):
        english_text, english_ref, version_label = _get_english(
            book_code, chapter, verse, english_version)

    # Pick the primary reference for display
    ref = tamil_ref if display_mode == "tamil" else english_ref

    return {
        "book_code":      book_code,
        "chapter":        chapter,
        "verse":          verse,
        "reference":      ref,
        "tamil_ref":      tamil_ref,
        "english_ref":    english_ref,
        "tamil_text":     tamil_text,
        "english_text":   english_text,
        "display_mode":   display_mode,
        "english_version": version_label,
        "found": bool(tamil_text or english_text),
    }