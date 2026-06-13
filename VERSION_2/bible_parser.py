import re

# Bible book name mappings
BOOK_NAMES = {
    # English
    "genesis": "Genesis", "gen": "Genesis",
    "exodus": "Exodus", "exo": "Exodus",
    "psalm": "Psalms", "psalms": "Psalms",
    "proverbs": "Proverbs", "prov": "Proverbs",
    "isaiah": "Isaiah", "isa": "Isaiah",
    "jeremiah": "Jeremiah", "jer": "Jeremiah",
    "matthew": "Matthew", "mat": "Matthew",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "romans": "Romans", "rom": "Romans",
    "philippians": "Philippians", "phil": "Philippians",
    "revelation": "Revelation", "rev": "Revelation",
    # Tamil
    "யோவான்": "John",
    "மத்தேயு": "Matthew",
    "ஆதியாகமம்": "Genesis",
    "சங்கீதம்": "Psalms",
    "ரோமர்": "Romans",
    "பிலிப்பியர்": "Philippians",
    "ஏசாயா": "Isaiah",
    "எரேமியா": "Jeremiah",
    "நீதிமொழிகள்": "Proverbs",
    "வெளிப்படுத்தல்": "Revelation",
}

def parse_reference(text):
    text = text.lower().strip()

    # Pattern: "john chapter 3 verse 16" or "john 3 16" or "john 3:16"
    pattern = r'(\w+)\s+(?:chapter\s+)?(\d+)\s+(?:verse\s+)?(\d+)'
    match = re.search(pattern, text)

    if match:
        book_raw = match.group(1)
        chapter = int(match.group(2))
        verse = int(match.group(3))
        book = BOOK_NAMES.get(book_raw, book_raw.capitalize())
        return {"book": book, "chapter": chapter, "verse": verse}

    return None