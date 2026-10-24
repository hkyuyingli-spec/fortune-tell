"""
fix_translations.py - replace pinyin in interpretation.py with meaning-based labels.

Run from the project folder (same folder as interpretation.py and glossary.py):
    python fix_translations.py

What it does:
  1. Makes a timestamped backup of interpretation.py
  2. For every entry shaped like  "天同": {"zh": "天同", "en": "...", "id": "..."}
     sets en / id from glossary.py
  3. Prints what was updated, and lists entries it could not judge so you can check them
Nothing else in the file is touched.
"""
import datetime
import re
import shutil
import sys

from glossary import ENTRIES, STEMS, BRANCHES

FILE = "interpretation.py"

try:
    text = open(FILE, encoding="utf-8").read()
except FileNotFoundError:
    sys.exit("Cannot find %s. Run this script from the project folder." % FILE)

backup = "%s.bak_%s" % (FILE, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
shutil.copy(FILE, backup)
print("Backup saved as", backup)

updated, missing = [], []
for e in ENTRIES:
    done = False
    for k in [e["zh"], *e["aliases"]]:
        pattern = (r'("%s"\s*:\s*\{\s*"zh"\s*:\s*"[^"]*"\s*,\s*"en"\s*:\s*")[^"]*'
                   r'(",\s*"id"\s*:\s*")[^"]*(")') % re.escape(k)
        text, n = re.subn(pattern, lambda m: m.group(1) + e["en"] + m.group(2) + e["id"] + m.group(3), text)
        if n:
            done = True
    (updated if done else missing).append(e["zh"] + ("  (review)" if e["review"] and done else ""))

# ---- BaZi stems and branches ----
for table in (STEMS, BRANCHES):
    for zh, (en, idn) in table.items():
        pattern = (r'("%s"\s*:\s*\{\s*"zh"\s*:\s*"[^"]*"\s*,\s*"en"\s*:\s*")[^"]*'
                   r'(",\s*"id"\s*:\s*")[^"]*(")') % re.escape(zh)
        text, n = re.subn(pattern, lambda m: m.group(1) + en + m.group(2) + idn + m.group(3), text)
        (updated if n else missing).append(zh)

open(FILE, "w", encoding="utf-8").write(text)

print("\nUPDATED (%d):" % len(updated))
for z in updated:
    print("  ", z)
print("\nNot present in this file (normal for terms stored elsewhere): %d" % len(missing))
print("  ", " ".join(missing))

# ---- audit: entries that still look untranslated ----
pinyin_words = {e["pinyin"].lower() for e in ENTRIES}
triples = re.findall(r'"zh"\s*:\s*"([^"]*)"\s*,\s*"en"\s*:\s*"([^"]*)"\s*,\s*"id"\s*:\s*"([^"]*)"', text)
suspect = []
for zh, en, idn in triples:
    if not re.search(r"[\u4e00-\u9fff]", zh):
        continue
    if en.lower() in pinyin_words or idn.lower() in pinyin_words or (en == idn and en.isascii() and en != zh):
        suspect.append((zh, en, idn))

print("\nPLEASE CHECK - entries that may still be pinyin (%d):" % len(suspect))
if suspect:
    for zh, en, idn in suspect:
        print("   %s | en=%s | id=%s" % (zh, en, idn))
    print("Send this list to Claude and the labels will be added to glossary.py.")
else:
    print("   none found")

print("\nDone. Restart the Streamlit app and switch language to English to check.")
print("To undo: copy %s back over %s" % (backup, FILE))
