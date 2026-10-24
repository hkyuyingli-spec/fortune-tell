"""
apply_beta_patch.py - shows the beta statement in app.py (two small edits).
Run once in the project folder:   python apply_beta_patch.py
Makes a backup first, and refuses to change anything if it cannot find the exact lines.
"""
import datetime
import shutil
import sys

FILE = "app.py"
raw = open(FILE, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"

if "beta_notice" in raw:
    sys.exit("app.py already contains beta_notice - nothing to do.")

imp_old = "import period_engine as pe" + nl
imp_new = imp_old + "import beta_notice as bn" + nl
cap_old = 'st.caption(t("app_caption", lang))' + nl
cap_new = cap_old + "bn.render_beta_notice(st, lang)" + nl

for name, old in (("import line", imp_old), ("app caption line", cap_old)):
    n = raw.count(old)
    if n != 1:
        sys.exit("Cannot find the %s exactly once (found %d). app.py was NOT changed." % (name, n))

backup = "app.py.bak_%s" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(FILE, backup)
raw = raw.replace(imp_old, imp_new, 1).replace(cap_old, cap_new, 1)
open(FILE, "w", encoding="utf-8", newline="").write(raw)
print("Done. Backup:", backup)
print("Next: restart Streamlit; the beta statement appears under the title.")
