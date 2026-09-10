# Short, templated interpretation content keyed off real chart data.
# This is structured/templated text (like Click108's own interpretations),
# not a claim of scientific validity.

DAY_MASTER_BLURB = {
    "甲": "像一棵挺立的大樹：正直、有領導欲，喜歡開創局面，但有時稍嫌固執。",
    "乙": "像柔韌的花草：適應力強、心思細膩，善於在複雜關係中找到生存空間。",
    "丙": "像太陽：熱情外向、行動力強，天生的焦點人物，但耐性有待磨練。",
    "丁": "像燭火：溫暖細緻、重感情，善於在小範圍內發揮深刻的影響力。",
    "戊": "像高山：穩重可靠、責任感重，是團隊中值得信賴的支柱。",
    "己": "像田地：包容務實、善於培養他人，安全感需求較高。",
    "庚": "像刀劍：果斷剛毅、原則性強，行事直接，不擅長拐彎抹角。",
    "辛": "像珠寶：講究細節、追求完美，對自己與他人要求都不低。",
    "壬": "像江河：聰明善變、視野開闊，喜歡自由，不受拘束。",
    "癸": "像雨露：溫和內斂、直覺敏銳，善於體察他人情緒。",
}

MAJOR_STAR_BLURB = {
    "紫微": "領導格局，重視地位與尊嚴，天生带著一種「帝王氣」，喜歡掌控大局。",
    "天機": "腦筋轉得快，善謀略、點子多，但也容易多想，情緒隨思緒起伏。",
    "太陽": "光明磊落、熱心公益，付出型人格，格外在意是否「被看見」。",
    "武曲": "務實剛毅，執行力強，是天生的財務與行動派，情感表達較內斂。",
    "天同": "溫和知足，重視生活品質與情感和諧，抗壓性需要後天培養。",
    "廉貞": "個性複雜多面，理性與感性交織，桃花與事業心並存。",
    "天府": "穩重厚道，善於守成與理財，是可靠的「大管家」型人物。",
    "太陰": "細膩內斂，重視家庭與內在世界，情感豐富但不輕易外露。",
    "貪狼": "多才多藝、社交手腕靈活，慾望與才華並重，人生選項多。",
    "巨門": "口才犀利、分析力強，適合靠語言、專業吃飯，也容易因言惹議。",
    "天相": "溫和公正，重視形象與服務精神，是天生的協調者。",
    "天梁": "老成持重，樂於照顧他人，常扮演長輩或貴人的角色。",
    "七殺": "行動派、敢衝敢拚，人生起伏較大，適合開創型事業。",
    "破軍": "破舊立新、不安於現狀，變動與挑戰是這個格局的常態。",
}

BUREAU_BLURB = {
    "水": "水二局：人生節奏偏快起步，早年較早經歷變動與磨練。",
    "木": "木三局：成長節奏中庸，穩紮穩打型的人生曲線。",
    "金": "金四局：性格中帶著一份韌性，需要時間淬鍊才能顯出光芒。",
    "土": "土五局：大器晚成的格局，中年之後的發展往往更為扎實。",
    "火": "火六局：人生起伏較為明顯，需要學習在高峰與低谷間找到平衡。",
}

PALACE_MEANING = {
    "命宮": "你的核心性格與人生基調",
    "兄弟": "手足情誼與合夥關係",
    "夫妻": "感情觀與婚姻狀態",
    "子女": "子女緣分與創造力",
    "財帛": "賺錢方式與金錢觀",
    "疾厄": "健康體質與壓力反應",
    "遷移": "外出運與人際際遇",
    "交友": "朋友圈與人脈資源",
    "官祿": "事業發展與職場定位",
    "田宅": "不動產運與居家生活",
    "福德": "精神生活與福氣厚薄",
    "父母": "與父母長輩的緣分",
}


def free_tier_summary(bazi_pillars, day_master, ziwei):
    life_row = ziwei.palace_table()[0]
    star_text = "、".join(life_row["stars"]) if life_row["stars"] else "（本宮無主星，個性受對宮及三方影響較大）"
    day_stem = bazi_pillars["day"][0]
    lines = [
        f"**你的四柱八字**：{bazi_pillars['year']} {bazi_pillars['month']} {bazi_pillars['day']} {bazi_pillars['hour']}",
        f"**日主（代表你自己）**：{day_stem} — {DAY_MASTER_BLURB.get(day_stem, '')}",
        f"**命宮**：{life_row['stem']}{life_row['branch']}，主星為 {star_text}",
        f"**命主 / 身主**：{ziwei.ming_zhu} / {ziwei.shen_zhu}",
        f"**五行局**：{ziwei.bureau_name} — {BUREAU_BLURB.get(ziwei.bureau_element, '')}",
    ]
    if life_row["stars"]:
        lines.append("**命宮主星解讀**：" + " ".join(MAJOR_STAR_BLURB.get(s, "") for s in life_row["stars"]))
    return "\n\n".join(lines)


def paid_tier_report(ziwei, current_year=None):
    rows = ziwei.palace_table()
    out = []
    for row in rows:
        stars = "、".join(row["stars"]) if row["stars"] else "無主星"
        blurb = " ".join(MAJOR_STAR_BLURB.get(s, "") for s in row["stars"]) or "此宮由對宮及三方四正的星曜影響較大，建議合併命宮一起看。"
        body_tag = "（身宮）" if row["is_body_palace"] else ""
        d_start, d_end = row["decade"]["range"]
        out.append({
            "palace": row["palace"] + body_tag,
            "meaning": PALACE_MEANING.get(row["palace"], ""),
            "stem_branch": row["stem"] + row["branch"],
            "stars": stars,
            "blurb": blurb,
            "decade_range": f"{d_start}–{d_end} 歲",
        })
    current_palace = ziwei.current_year_palace(current_year) if current_year else None
    return out, current_palace
