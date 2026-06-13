import json
import os

# We'll use a free Bible JSON file
# Download from: https://github.com/thiagobodruk/bible/tree/master/json
# Save as bible_en.json in your V2 folder

def load_bible(path="./bible_en.json"):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

BIBLE = load_bible()

def get_verse(book, chapter, verse):
    if not BIBLE:
        return "Bible database not loaded."
    try:
        for b in BIBLE:
            if b["name"].lower() == book.lower():
                return b["chapters"][chapter - 1][verse - 1]
    except (IndexError, KeyError):
        return "Verse not found."
    return "Book not found."