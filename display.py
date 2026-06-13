from parser import get_genre

GENRE_THEMES = {
    "law":        {"label":"The Law",              "accent":"#d4873a","particle":"✦",
                   "bg_image":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80","overlay":"rgba(20,8,0,0.78)"},
    "history":    {"label":"Historical Books",     "accent":"#7ec87e","particle":"❧",
                   "bg_image":"https://images.unsplash.com/photo-1476231682828-37e571bc172f?w=1920&q=80","overlay":"rgba(10,25,10,0.80)"},
    "poetry":     {"label":"Poetry & Wisdom",      "accent":"#a0a8ff","particle":"✿",
                   "bg_image":"https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1920&q=80","overlay":"rgba(5,5,20,0.82)"},
    "prophecy":   {"label":"The Prophets",         "accent":"#ffb347","particle":"⚡",
                   "bg_image":"https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9?w=1920&q=80","overlay":"rgba(18,8,0,0.80)"},
    "gospel":     {"label":"The Gospels",          "accent":"#5bc8ff","particle":"✝",
                   "bg_image":"https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1920&q=80","overlay":"rgba(0,8,20,0.80)"},
    "acts":       {"label":"Acts of the Apostles", "accent":"#ff80ff","particle":"🔥",
                   "bg_image":"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80","overlay":"rgba(15,0,15,0.82)"},
    "epistle":    {"label":"The Epistles",         "accent":"#40e0a0","particle":"✉",
                   "bg_image":"https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=1920&q=80","overlay":"rgba(0,15,10,0.80)"},
    "apocalyptic":{"label":"Revelation",           "accent":"#ff4040","particle":"★",
                   "bg_image":"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80","overlay":"rgba(20,0,0,0.82)"},
}

def show_verse(verse_data: dict) -> dict:
    book_code = verse_data.get("book_code", "Joh")
    genre     = get_genre(book_code)
    theme     = GENRE_THEMES.get(genre, GENRE_THEMES["gospel"])
    return {
        "book_code":      book_code,
        "reference":      verse_data.get("reference", ""),
        "tamil_ref":      verse_data.get("tamil_ref", ""),
        "english_ref":    verse_data.get("english_ref", ""),
        "tamil_text":     verse_data.get("tamil_text", ""),
        "english_text":   verse_data.get("english_text", ""),
        "display_mode":   verse_data.get("display_mode", "both"),
        "english_version":verse_data.get("english_version", ""),
        "found":          verse_data.get("found", False),
        "theme":          theme,
    }