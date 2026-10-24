"""
compare_natal_vs_iztro.py - checks YOUR real chart engine against iztro on 1,450 reference births.

Run in the project folder (needs natal_reference_cases.json next to it):
    python compare_natal_vs_iztro.py

For each birth it compares: bureau, Life ruler, Body ruler, and for all 12 palaces the
stem+branch, the 14 major stars, the Body palace flag and the 10-year cycle range.
Cases include random births, births within 3 days of Chinese New Year, births in leap months,
and births in the late-night (23:00) and early (00:xx) Zi hour.
"""
import json
import os
import sys
from collections import Counter, defaultdict

from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart

HERE = os.path.dirname(os.path.abspath(__file__))
cases = json.load(open(os.path.join(HERE, "natal_reference_cases.json"), encoding="utf-8"))
ALIAS = {"僕役": "交友", "仆役": "交友"}

by_cat_total, by_cat_bad = Counter(), Counter()
by_field = Counter()
examples = defaultdict(list)
errors = []

for c in cases:
    cat = c["cat"]
    by_cat_total[cat] += 1
    try:
        bc = BirthChart(c["y"], c["m"], c["d"], c["hour"], c["minute"])
        zw = ZiWeiChart(bc, c["gender"])
        rows = {r["palace"]: r for r in zw.palace_table()}
        exp = c["expected"]
        problems = []

        if zw.bureau_name != exp["bureau"]:
            problems.append(("bureau", zw.bureau_name, exp["bureau"]))
        if zw.ming_zhu != exp["ming_zhu"]:
            problems.append(("ming_zhu", zw.ming_zhu, exp["ming_zhu"]))
        if zw.shen_zhu != exp["shen_zhu"]:
            problems.append(("shen_zhu", zw.shen_zhu, exp["shen_zhu"]))

        for p in exp["palaces"]:
            name = ALIAS.get(p["name"], p["name"])
            r = rows.get(name)
            if r is None:
                problems.append(("palace_missing", name, "present"))
                continue
            if (r["stem"], r["branch"]) != (p["stem"], p["branch"]):
                problems.append(("stem_branch", name + ":" + r["stem"] + r["branch"], p["stem"] + p["branch"]))
            if sorted(r["stars"]) != sorted(p["stars"]):
                problems.append(("major_stars", name + ":" + ",".join(r["stars"]), ",".join(p["stars"])))
            if bool(r["is_body_palace"]) != bool(p["body"]):
                problems.append(("body_palace", name, str(p["body"])))
            if tuple(r["decade"]["range"]) != tuple(p["range"]):
                problems.append(("decade_range", name + ":" + str(tuple(r["decade"]["range"])), str(tuple(p["range"]))))

        if problems:
            by_cat_bad[cat] += 1
            for f, _, _ in problems:
                by_field[f] += 1
            if len(examples[cat]) < 3:
                examples[cat].append((c, problems[:4]))
    except Exception as e:  # keep going, report at the end
        by_cat_bad[cat] += 1
        by_field["exception"] += 1
        if len(errors) < 5:
            errors.append((c, repr(e)))

total, bad = sum(by_cat_total.values()), sum(by_cat_bad.values())
print("=" * 60)
print("Births checked:", total, "| births with at least one difference:", bad)
print("-" * 60)
for cat in by_cat_total:
    print("%-14s %4d checked, %4d differ" % (cat, by_cat_total[cat], by_cat_bad[cat]))
print("-" * 60)
print("Differences by field:", dict(by_field) if by_field else "none")
for cat, items in examples.items():
    print("\nExamples (%s):" % cat)
    for c, probs in items:
        print("  born %s-%s-%s %02d:%02d %s" % (c["y"], c["m"], c["d"], c["hour"], c["minute"], c["gender"]))
        for f, mine, ref in probs:
            print("     %-13s yours=%s  iztro=%s" % (f, mine, ref))
for c, e in errors:
    print("\nERROR for", c["y"], c["m"], c["d"], c["hour"], ":", e)
print("=" * 60)
print("RESULT:", "ALL MATCH" if bad == 0 else "DIFFERENCES FOUND - paste this output to Claude")
sys.exit(0 if bad == 0 else 1)
