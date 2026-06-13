import pandas as pd
import re

data = []

with open("TAMOVR-BibleWorks.txt.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        # Example format: John 3:16 text...
        match = re.match(r'([A-Za-z]+)\s(\d+):(\d+)\s(.+)', line)

        if match:
            book, chapter, verse, text = match.groups()
            data.append([book, int(chapter), int(verse), text])

df = pd.DataFrame(data, columns=["Book","Chapter","Verse","Text_English"])

df.to_csv("data_cleaning.csv", index=False)

print("✅ CSV created")