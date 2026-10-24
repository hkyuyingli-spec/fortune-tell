"""
apply_time_fixes.py - applies the time fixes (run once, in the project folder):

  1. calendar_engine.py : leap-month rule now matches iztro for late-night Zi (23:00-23:59) births
  2. app.py             : adds the birth time zone selector, converts the clock time to standard
                          time (daylight saving removed) and shows the time notes

Needs time_engine.py in the same folder.   Run:  python apply_time_fixes.py
It checks that every line it needs exists exactly once BEFORE changing anything, and makes backups.
"""
import datetime
import os
import shutil
import sys


def read(path):
    raw = open(path, encoding="utf-8", newline="").read()
    return raw, ("\r\n" if "\r\n" in raw else "\n")


if not os.path.exists("time_engine.py"):
    sys.exit("time_engine.py is missing from this folder. Save it here first.")

cal, cnl = read("calendar_engine.py")
app, anl = read("app.py")
plan = []   # (file, text, newline, [(name, old, new)])

# ---- calendar_engine.py ----
cal_old = "            if self.lunar_day > 15:" + cnl
cal_new = ("            # iztro convention: the second-half-of-leap-month rule is not applied to" + cnl +
           "            # late-night Zi (23:00-23:59) births." + cnl +
           "            if self.lunar_day > 15 and not self.is_late_zi:" + cnl)
cal_edits = [] if "not self.is_late_zi:" in cal else [("leap-month rule line", cal_old, cal_new)]

# ---- app.py ----
n = anl
a_edits = []
if "time_engine" not in app:
    a_edits = [
        ("import line", "import firebase_db" + n,
         "import firebase_db" + n + "import time_engine as te" + n),
        ("birth time input line",
         '        birth_time = st.time_input(t("birth_time", lang), value=datetime.time(12, 0))' + n,
         '        birth_time = st.time_input(t("birth_time", lang), value=datetime.time(12, 0))' + n +
         "        birth_tz = te.render_timezone_select(st, lang)" + n),
        ("chart input line",
         '            st.session_state["chart_input"] = (birth_date, birth_time, gender)' + n,
         "            birth_date, birth_time, _tz_info = te.apply_birth_timezone(birth_date, birth_time, birth_tz)" + n +
         "            te.store_time_info(st, _tz_info, birth_time)" + n +
         '            st.session_state["chart_input"] = (birth_date, birth_time, gender)' + n),
        ("report call line",
         "        render_full_report(bc, zw, lang)" + n,
         "        te.render_time_notes(st, lang)" + n + "        render_full_report(bc, zw, lang)" + n),
    ]

problems = []
for fname, text, edits in (("calendar_engine.py", cal, cal_edits), ("app.py", app, a_edits)):
    for name, old, _ in edits:
        c = text.count(old)
        if c != 1:
            problems.append("%s: cannot find the %s exactly once (found %d)" % (fname, name, c))
if problems:
    sys.exit("NOTHING WAS CHANGED.\n" + "\n".join(problems) + "\nSend me that part of the file.")
if not cal_edits and not a_edits:
    sys.exit("Both files are already patched - nothing to do.")

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for fname, text, nl, edits in (("calendar_engine.py", cal, cnl, cal_edits), ("app.py", app, anl, a_edits)):
    if not edits:
        print(fname, ": already patched, skipped")
        continue
    shutil.copy(fname, "%s.bak_%s" % (fname, stamp))
    for _, old, new in edits:
        text = text.replace(old, new, 1)
    open(fname, "w", encoding="utf-8", newline="").write(text)
    print(fname, ": done (backup %s.bak_%s)" % (fname, stamp))
print("Next: python test_time_engine.py, then restart Streamlit.")
