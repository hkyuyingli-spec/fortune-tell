import json
from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart

with open("reference_latezi.json", encoding="utf-8") as f:
    cases = json.load(f)

PALACE_NAME_ALIAS = {"僕役": "交友"}

total = 0
passed = 0
mismatches = []

for c in cases:
    if "error" in c:
        continue
    inp = c["input"]
    y, m, d = map(int, inp["date"].split("-"))
    gender = inp["gender"]
    total += 1

    try:
        bc = BirthChart(y, m, d, 23, 30)  # late-zi: 23:00-23:59
        zw = ZiWeiChart(bc, gender)
    except Exception as e:
        mismatches.append({"input": inp, "error": f"exception: {e}"})
        continue

    ok = True
    reasons = []
    if zw.bureau_name != c["fiveElementsClass"]:
        ok = False
        reasons.append(f"bureau: ours={zw.bureau_name} ref={c['fiveElementsClass']}")
    if zw.soul_branch != c["soulBranch"]:
        ok = False
        reasons.append(f"soul_branch: ours={zw.soul_branch} ref={c['soulBranch']}")
    if zw.ming_zhu != c["soulStar"]:
        ok = False
        reasons.append(f"ming_zhu: ours={zw.ming_zhu} ref={c['soulStar']}")
    if zw.shen_zhu != c["bodyStar"]:
        ok = False
        reasons.append(f"shen_zhu: ours={zw.shen_zhu} ref={c['bodyStar']}")

    ref_palaces = {PALACE_NAME_ALIAS.get(p["name"], p["name"]): p for p in c["palaces"]}
    for row in zw.palace_table():
        ref = ref_palaces.get(row["palace"])
        if ref is None:
            ok = False
            reasons.append(f"missing ref palace {row['palace']}")
            continue
        if row["stem"] + row["branch"] != ref["gz"]:
            ok = False
            reasons.append(f"{row['palace']} gz: ours={row['stem']}{row['branch']} ref={ref['gz']}")
        our_stars = sorted(row["stars"])
        if our_stars != ref["stars"]:
            ok = False
            reasons.append(f"{row['palace']} stars: ours={our_stars} ref={ref['stars']}")

    if ok:
        passed += 1
    else:
        mismatches.append({"input": inp, "reasons": reasons})

print(f"LATE-ZI SWEEP: PASSED {passed}/{total}")
for mm in mismatches[:10]:
    print(mm)
