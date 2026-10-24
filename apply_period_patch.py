"""
apply_period_patch.py - adds the period selector to app.py (two small edits).

Run once, in the project folder:   python apply_period_patch.py
  1. makes a backup of app.py
  2. adds   import period_engine as pe
  3. adds   pe.render_period_selector(st, bc, zw, lang)   above the topic buttons
It refuses to change anything if it cannot find the exact lines.
"""
import datetime
import shutil
import sys

FILE = "app.py"
raw = open(FILE, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"

if "period_engine" in raw:
    sys.exit("app.py already contains period_engine - nothing to do.")

imp_old = "import firebase_db" + nl
imp_new = "import firebase_db" + nl + "import period_engine as pe" + nl
cap_old = '    st.caption(t("ai_category_header", lang))' + nl
cap_new = ("    pe.render_period_selector(st, bc, zw, lang)" + nl + nl + cap_old)

for name, old in (("import line", imp_old), ("topic caption line", cap_old)):
    n = raw.count(old)
    if n != 1:
        sys.exit("Cannot find the %s exactly once (found %d). app.py was NOT changed. "
                 "Send me that part of app.py." % (name, n))

backup = "app.py.bak_%s" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(FILE, backup)
raw = raw.replace(imp_old, imp_new, 1).replace(cap_old, cap_new, 1)
open(FILE, "w", encoding="utf-8", newline="").write(raw)
print("Done. Backup:", backup)
print("Next: restart Streamlit and open the AI chat section.")
