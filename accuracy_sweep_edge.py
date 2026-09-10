import json
from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart, PALACE_NAMES

with open("reference_leap_edge.json", encoding="utf-8") as f:
    cases = json.load(f)

BUREAU_NAME_MAP = {  # iztro's fiveElementsClass label -> our bureau_name label
    "水二局": "水二局", "木三局": "木三局", "金四局": "金四局", "土五局": "土五局", "火六局": "火六局",
}
# iztro palace names -> ours (交友 vs 仆役 naming variant)
PALACE_NAME_ALIAS = {"僕役": "交友"}

def hour_from_timeindex(ti):
    # inverse of hour_to_shichen_index (approx): map shichen index back to a representative hour
    # index0=23:00-00:59 -> use 0, index k (k=1..11) -> use (2k-1) i.e. midpoint hour of the block
    if ti == 0:
        return 0
    return 2 * ti - 1  # e.g. ti=1 -> hour1 (01:00), ti=6->hour11(11:00), ti=11->hour21(21:00)

total = 0
passed = 0
mismatches = []

for c in cases:
    if "error" in c:
        continue
    inp = c["input"]
    y, m, d = map(int, inp["date"].split("-"))
    hour = hour_from_timeindex(inp["timeIndex"])
    gender = inp["gender"]
    total += 1

    try:
        bc = BirthChart(y, m, d, hour, 0)
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

    our_body_branch = None
    for row in zw.palace_table():
        if row["is_body_palace"]:
            our_body_branch = row["branch"]
    if our_body_branch != c["bodyBranch"]:
        ok = False
        reasons.append(f"body_branch: ours={our_body_branch} ref={c['bodyBranch']}")

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
        if ref["decadeRange"] and list(row["decade"]["range"]) != ref["decadeRange"]:
            ok = False
            reasons.append(f"{row['palace']} decade: ours={row['decade']['range']} ref={ref['decadeRange']}")

    if ok:
        passed += 1
    else:
        mismatches.append({"input": inp, "reasons": reasons})

print(f"PASSED {passed}/{total}")
for mm in mismatches[:10]:
    print(mm)
