import re

word_to_num = {
    "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,
    "six":6,"seven":7,"eight":8,"nine":9,"ten":10,
    "eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
    "fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,
    "nineteen":19,"twenty":20,"thirty":30,"forty":40,
    "fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100,
}

tamil_num_words = {
    "ஒன்று":1,"ஒன்றாம்":1,"ஒன்றாவது":1,"முதல்":1,"முதலாம்":1,"முதலாவது":1,
    "இரண்டு":2,"இரண்டாம்":2,"இரண்டாவது":2,
    "மூன்று":3,"மூன்றாம்":3,"மூன்றாவது":3,
    "நான்கு":4,"நான்காம்":4,"நான்காவது":4,
    "ஐந்து":5,"ஐந்தாம்":5,"ஐந்தாவது":5,
    "ஆறு":6,"ஆறாம்":6,"ஆறாவது":6,
    "ஏழு":7,"ஏழாம்":7,"ஏழாவது":7,
    "எட்டு":8,"எட்டாம்":8,"எட்டாவது":8,
    "ஒன்பது":9,"ஒன்பதாம்":9,"ஒன்பதாவது":9,
    "பத்து":10,"பத்தாம்":10,"பத்தாவது":10,
    "பதினொன்று":11,"பதினொன்றாம்":11,"பதினொன்றாவது":11,
    "பன்னிரண்டு":12,"பன்னிரண்டாம்":12,"பன்னிரண்டாவது":12,
    "பதின்மூன்று":13,"பதின்மூன்றாம்":13,"பதின்மூன்றாவது":13,
    "பதினான்கு":14,"பதினான்காம்":14,"பதினான்காவது":14,
    "பதினைந்து":15,"பதினைந்தாம்":15,"பதினைந்தாவது":15,
    "பதினாறு":16,"பதினாறாம்":16,"பதினாறாவது":16,
    "பதினேழு":17,"பதினேழாம்":17,"பதினேழாவது":17,
    "பதினெட்டு":18,"பதினெட்டாம்":18,"பதினெட்டாவது":18,
    "பத்தொன்பது":19,"பத்தொன்பதாம்":19,"பத்தொன்பதாவது":19,
    "இருபது":20,"இருபதாம்":20,"இருபதாவது":20,
    "இருபத்தொன்று":21,"இருபத்திரண்டு":22,"இருபத்துமூன்று":23,
    "இருபத்தினான்கு":24,"இருபத்தைந்து":25,"இருபத்தாறு":26,
    "இருபத்தேழு":27,"இருபத்தெட்டு":28,"இருபத்தொன்பது":29,
    "முப்பது":30,"முப்பதாம்":30,"முப்பதாவது":30,
    "முப்பத்தொன்று":31,"முப்பத்திரண்டு":32,"முப்பத்துமூன்று":33,
    "நாற்பது":40,"நாற்பதாம்":40,"நாற்பதாவது":40,
    "ஐம்பது":50,"ஐம்பதாம்":50,"ஐம்பதாவது":50,
    "அறுபது":60,"எழுபது":70,"எண்பது":80,"தொண்ணூறு":90,"நூறு":100,
}

TAMIL_NOISE = [
    "அதிகாரம்","வசனம்","ஆகமம்","திருவசனம்",
    "வாசிக்கிறோம்","வாசிப்போம்","படிக்கிறோம்","சொல்கிறது",
]

tamil_book_names = {
    "ஆதியாகமம்":"genesis","ஆதி":"genesis",
    "யாத்திராகமம்":"exodus","யாத்":"exodus",
    "லேவியராகமம்":"leviticus","எண்ணாகமம்":"numbers",
    "உபாகமம்":"deuteronomy","யோசுவா":"joshua",
    "நியாயாதிபதிகள்":"judges","ரூத்":"ruth",
    "1 சாமுவேல்":"1 samuel","1சாமுவேல்":"1 samuel",
    "2 சாமுவேல்":"2 samuel","2சாமுவேல்":"2 samuel",
    "1 இராஜாக்கள்":"1 kings","1இராஜாக்கள்":"1 kings",
    "2 இராஜாக்கள்":"2 kings","2இராஜாக்கள்":"2 kings",
    "1 நாளாகமம்":"1 chronicles","2 நாளாகமம்":"2 chronicles",
    "எஸ்றா":"ezra","நெகேமியா":"nehemiah","எஸ்தர்":"esther",
    "யோபு":"job","சங்கீதம்":"psalms","சங்கீதங்கள்":"psalms",
    "நீதிமொழிகள்":"proverbs","பிரசங்கி":"ecclesiastes",
    "உன்னதப்பாட்டு":"song of solomon",
    "ஏசாயா":"isaiah","எரேமியா":"jeremiah","புலம்பல்":"lamentations",
    "எசேக்கியேல்":"ezekiel","தானியேல்":"daniel","ஓசியா":"hosea",
    "யோவேல்":"joel","ஆமோஸ்":"amos","ஒபதியா":"obadiah",
    "யோனா":"jonah","மீகா":"micah","நாகூம்":"nahum",
    "ஆபகூக்":"habakkuk","செப்பனியா":"zephaniah","ஆகாய்":"haggai",
    "சகரியா":"zechariah","மல்கியா":"malachi",
    "மத்தேயு":"matthew","மாற்கு":"mark","லூக்கா":"luke",
    "யோவான்":"john","அப்போஸ்தலர்":"acts","ரோமர்":"romans",
    "1 கொரிந்தியர்":"1 corinthians","1கொரிந்தியர்":"1 corinthians",
    "2 கொரிந்தியர்":"2 corinthians","2கொரிந்தியர்":"2 corinthians",
    "கலாத்தியர்":"galatians","எபேசியர்":"ephesians",
    "பிலிப்பியர்":"philippians","கொலோசியர்":"colossians",
    "1 தெசலோனிக்கேயர்":"1 thessalonians",
    "2 தெசலோனிக்கேயர்":"2 thessalonians",
    "1 தீமோத்தேயு":"1 timothy","2 தீமோத்தேயு":"2 timothy",
    "தீத்து":"titus","பிலேமோன்":"philemon","எபிரேயர்":"hebrews",
    "யாக்கோபு":"james","1 பேதுரு":"1 peter","2 பேதுரு":"2 peter",
    "1 யோவான்":"1 john","2 யோவான்":"2 john","3 யோவான்":"3 john",
    "யூதா":"jude","வெளிப்படுத்தல்":"revelation","வெளிப்படுத்துதல்":"revelation",
}

book_map = {
    "genesis":"Gen","exodus":"Exo","leviticus":"Lev","numbers":"Num",
    "deuteronomy":"Deu","joshua":"Jos","judges":"Jdg","ruth":"Rut",
    "1 samuel":"1Sa","2 samuel":"2Sa","1 kings":"1Ki","2 kings":"2Ki",
    "1 chronicles":"1Ch","2 chronicles":"2Ch","ezra":"Ezr",
    "nehemiah":"Neh","esther":"Est","job":"Job","psalms":"Psa",
    "proverbs":"Pro","ecclesiastes":"Ecc","song of solomon":"Son",
    "isaiah":"Isa","jeremiah":"Jer","lamentations":"Lam",
    "ezekiel":"Eze","daniel":"Dan","hosea":"Hos","joel":"Joe",
    "amos":"Amo","obadiah":"Oba","jonah":"Jon","micah":"Mic",
    "nahum":"Nah","habakkuk":"Hab","zephaniah":"Zep","haggai":"Hag",
    "zechariah":"Zec","malachi":"Mal","matthew":"Mat","mark":"Mar",
    "luke":"Luk","john":"Joh","acts":"Act","romans":"Rom",
    "1 corinthians":"1Co","2 corinthians":"2Co","galatians":"Gal",
    "ephesians":"Eph","philippians":"Phi","colossians":"Col",
    "1 thessalonians":"1Th","2 thessalonians":"2Th",
    "1 timothy":"1Ti","2 timothy":"2Ti","titus":"Tit","philemon":"Phm",
    "hebrews":"Heb","james":"Jam","1 peter":"1Pe","2 peter":"2Pe",
    "1 john":"1Jo","2 john":"2Jo","3 john":"3Jo","jude":"Jud","revelation":"Rev",
}

book_aliases = {
    "gen":"genesis","ex":"exodus","exod":"exodus","lev":"leviticus",
    "num":"numbers","deut":"deuteronomy","deu":"deuteronomy",
    "josh":"joshua","judg":"judges","jdg":"judges",
    "1sam":"1 samuel","2sam":"2 samuel","1ki":"1 kings","2ki":"2 kings",
    "1chr":"1 chronicles","2chr":"2 chronicles",
    "neh":"nehemiah","esth":"esther","ps":"psalms","psa":"psalms","psalm":"psalms",
    "prov":"proverbs","pro":"proverbs","eccl":"ecclesiastes","ecc":"ecclesiastes",
    "song":"song of solomon","sos":"song of solomon",
    "isa":"isaiah","jer":"jeremiah","lam":"lamentations",
    "ezek":"ezekiel","eze":"ezekiel","dan":"daniel",
    "hos":"hosea","zeph":"zephaniah","zec":"zechariah","mal":"malachi",
    "matt":"matthew","mat":"matthew","mk":"mark","mar":"mark",
    "lk":"luke","luk":"luke","jn":"john","joh":"john",
    "act":"acts","rom":"romans",
    "1cor":"1 corinthians","2cor":"2 corinthians",
    "gal":"galatians","eph":"ephesians","phil":"philippians","phi":"philippians",
    "col":"colossians","1thess":"1 thessalonians","2thess":"2 thessalonians",
    "1tim":"1 timothy","2tim":"2 timothy","tit":"titus","phm":"philemon",
    "heb":"hebrews","jas":"james","jam":"james",
    "1pet":"1 peter","2pet":"2 peter","1pe":"1 peter","2pe":"2 peter",
    "1jn":"1 john","2jn":"2 john","3jn":"3 john",
    "1jo":"1 john","2jo":"2 john","3jo":"3 john",
    "jude":"jude","rev":"revelation",
}

BOOK_CHAPTER_LIMITS = {
    "gen":50,"exo":40,"lev":27,"num":36,"deu":34,"jos":24,"jdg":21,"rut":4,
    "1sa":31,"2sa":24,"1ki":22,"2ki":25,"1ch":29,"2ch":36,"ezr":10,"neh":13,
    "est":10,"job":42,"psa":150,"pro":31,"ecc":12,"son":8,"isa":66,"jer":52,
    "lam":5,"eze":48,"dan":12,"hos":14,"joe":3,"amo":9,"oba":1,"jon":4,
    "mic":7,"nah":3,"hab":3,"zep":3,"hag":2,"zec":14,"mal":4,
    "mat":28,"mar":16,"luk":24,"joh":21,"act":28,"rom":16,"1co":16,"2co":13,
    "gal":6,"eph":6,"phi":4,"col":4,"1th":5,"2th":3,"1ti":6,"2ti":4,
    "tit":3,"phm":1,"heb":13,"jam":5,"1pe":5,"2pe":3,"1jo":5,"2jo":1,
    "3jo":1,"jud":1,"rev":22,
}

BOOK_GENRES = {
    "Gen":"law","Exo":"law","Lev":"law","Num":"law","Deu":"law",
    "Jos":"history","Jdg":"history","Rut":"history","1Sa":"history","2Sa":"history",
    "1Ki":"history","2Ki":"history","1Ch":"history","2Ch":"history",
    "Ezr":"history","Neh":"history","Est":"history",
    "Job":"poetry","Psa":"poetry","Pro":"poetry","Ecc":"poetry","Son":"poetry",
    "Isa":"prophecy","Jer":"prophecy","Lam":"prophecy","Eze":"prophecy","Dan":"prophecy",
    "Hos":"prophecy","Joe":"prophecy","Amo":"prophecy","Oba":"prophecy","Jon":"prophecy",
    "Mic":"prophecy","Nah":"prophecy","Hab":"prophecy","Zep":"prophecy",
    "Hag":"prophecy","Zec":"prophecy","Mal":"prophecy",
    "Mat":"gospel","Mar":"gospel","Luk":"gospel","Joh":"gospel","Act":"acts",
    "Rom":"epistle","1Co":"epistle","2Co":"epistle","Gal":"epistle","Eph":"epistle",
    "Phi":"epistle","Col":"epistle","1Th":"epistle","2Th":"epistle","1Ti":"epistle",
    "2Ti":"epistle","Tit":"epistle","Phm":"epistle","Heb":"epistle","Jam":"epistle",
    "1Pe":"epistle","2Pe":"epistle","1Jo":"epistle","2Jo":"epistle","3Jo":"epistle",
    "Jud":"epistle","Rev":"apocalyptic",
}

def _extract_tamil_numbers(text):
    positions = []
    temp = text
    for word in sorted(tamil_num_words, key=len, reverse=True):
        idx = temp.find(word)
        if idx != -1:
            positions.append((idx, tamil_num_words[word]))
            temp = temp.replace(word, " " * len(word), 1)
    positions.sort(key=lambda x: x[0])
    return [v for _, v in positions]

def _resolve_tamil_book(text):
    for name in sorted(tamil_book_names, key=len, reverse=True):
        if name in text:
            return text.replace(name, tamil_book_names[name]), True
    return text, False

def _smart_split(num, book_code):
    s = str(num)
    max_ch = BOOK_CHAPTER_LIMITS.get(book_code.lower(), 150)
    candidates = []
    for i in range(1, len(s)):
        ch, v = int(s[:i]), int(s[i:])
        if 1 <= ch <= max_ch and 1 <= v <= 176:
            candidates.append((ch, v))
    return max(candidates, key=lambda x: x[0]) if candidates else (None, None)

def parse_reference(text):
    if not text or not text.strip():
        return None, None, None
    text = text.strip()
    text, is_tamil = _resolve_tamil_book(text)
    tamil_numbers = _extract_tamil_numbers(text) if is_tamil else []
    if tamil_numbers:
        print(f"[Parser] Tamil numbers: {tamil_numbers}")

    text_lower = text.lower()
    for word in (["chapter","verse","the","of","adhikaram","vaakyam","vakyam","vasanam"] + TAMIL_NOISE):
        text_lower = text_lower.replace(word, " ")
    text_lower = re.sub(r'[\:\-\,]', ' ', text_lower)
    text_lower = re.sub(r'\s+', ' ', text_lower).strip()
    tokens = text_lower.split()

    words, digit_numbers, number_words = [], [], []
    for t in tokens:
        if re.match(r'^\d+$', t): digit_numbers.append(int(t))
        elif t in word_to_num: number_words.append(t)
        else: words.append(t)

    book_raw  = " ".join(words).strip()
    book_code = (book_map.get(book_raw)
                 or book_map.get(book_aliases.get(book_raw, "")) or None)
    if not book_code:
        for w in words:
            r = book_aliases.get(w)
            if r and r in book_map:
                book_code = book_map[r]; break
    if not book_code:
        book_code = book_raw.title()

    final = []
    if len(tamil_numbers) >= 2:
        final = list(tamil_numbers[:2])
        print(f"[Parser] Tamil → ch={final[0]}, v={final[1]}")
    elif digit_numbers:
        for num in digit_numbers:
            if num >= 100:
                ch, v = _smart_split(num, book_code)
                if ch: final.extend([ch, v])
                else:  final.append(num)
            else:
                final.append(num)
    elif number_words:
        total = current = 0
        for w in number_words:
            val = word_to_num.get(w, 0)
            if val == 100: current = current*100 if current else 100
            else: current += val
        total = total + current
        if total:
            if total >= 100:
                ch, v = _smart_split(total, book_code)
                if ch: final = [ch, v]
            else: final.append(total)
    elif len(tamil_numbers) == 1:
        final = tamil_numbers

    if len(final) < 2:
        print(f"[Parser] Could not extract ref from: '{text}'")
        return None, None, None

    print(f"[Parser] → {book_code} {final[0]}:{final[1]}")
    return book_code, final[0], final[1]

def get_genre(book_code):
    return BOOK_GENRES.get(book_code, "gospel")