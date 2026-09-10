from __future__ import annotations

MAJOR_STAR_BLURB = {
    "紫微": "紫微代表自我主體與人格光芒。",
    "天府": "天府代表穩定、內在安全感與資源整合。",
    "天機": "天機代表思維、觀察與靈感的流動。",
    "天相": "天相代表適應力、形象與人際反應。",
    "天梁": "天梁代表教養、信念與價值感。",
    "武曲": "武曲代表財務、決策與實際能力。",
    "太陽": "太陽代表能量、表達與目標方向。",
    "天同": "天同代表人際和諧與情感連結。",
    "廉貞": "廉貞代表變化、刺激與轉型動力。",
    "巨門": "巨門代表轉折、判斷與資訊處理。",
    "文昌": "文昌代表學習、靈性與內在安定。",
    "文曲": "文曲代表智慧、思辨與表達能力。",
}


def free_tier_summary(pillars, day_master, zw):
    return (
        f"此命盤的四柱為：{pillars['year'][0]}{pillars['year'][1]} / "
        f"{pillars['month'][0]}{pillars['month'][1]} / {pillars['day'][0]}{pillars['day'][1]} / "
        f"{pillars['time'][0]}{pillars['time'][1]}。\n"
        f"日主為 {day_master}，並以 {zw.bureau_number} 局作為簡要參考。"
    )


def paid_tier_report(zw, current_year):
    rows = []
    for idx, row in enumerate(zw.palace_table()):
        rows.append(
            {
                "palace": row["palace"],
                "meaning": row["meaning"],
                "stem_branch": f"{row['stem']}{row['branch']}",
                "stars": ", ".join(row["stars"]),
                "blurb": row["blurb"],
                "decade_range": f"{zw.decades_by_p[row['palace']]['range'][0]}–{zw.decades_by_p[row['palace']]['range'][1]} 歲",
            }
        )
    return rows, zw.soul_p
