# Templated interpretation content keyed off real chart data, in three
# languages. This is structured/templated text (like Click108's own
# interpretations), not a claim of scientific validity. en/id are
# functional translations -- worth a native-speaker pass before this
# faces a real paying audience, especially id (the actual target market;
# see earlier market research on the Indonesian weton/primbon gap).

DAY_MASTER_BLURB = {
    "甲": {"zh": "像一棵挺立的大樹：正直、有領導欲，喜歡開創局面，但有時稍嫌固執。",
           "en": "Yang Wood",
           "id": "Kayu Yang"},
    "乙": {"zh": "像柔韌的花草：適應力強、心思細膩，善於在複雜關係中找到生存空間。",
           "en": "Yin Wood",
           "id": "Kayu Yin"},
    "丙": {"zh": "像太陽：熱情外向、行動力強，天生的焦點人物，但耐性有待磨練。",
           "en": "Yang Fire",
           "id": "Api Yang"},
    "丁": {"zh": "像燭火：溫暖細緻、重感情，善於在小範圍內發揮深刻的影響力。",
           "en": "Yin Fire",
           "id": "Api Yin"},
    "戊": {"zh": "像高山：穩重可靠、責任感重，是團隊中值得信賴的支柱。",
           "en": "Yang Earth",
           "id": "Tanah Yang"},
    "己": {"zh": "像田地：包容務實、善於培養他人，安全感需求較高。",
           "en": "Yin Earth",
           "id": "Tanah Yin"},
    "庚": {"zh": "像刀劍：果斷剛毅、原則性強，行事直接，不擅長拐彎抹角。",
           "en": "Yang Metal",
           "id": "Logam Yang"},
    "辛": {"zh": "像珠寶：講究細節、追求完美，對自己與他人要求都不低。",
           "en": "Yin Metal",
           "id": "Logam Yin"},
    "壬": {"zh": "像江河：聰明善變、視野開闊，喜歡自由，不受拘束。",
           "en": "Yang Water",
           "id": "Air Yang"},
    "癸": {"zh": "像雨露：溫和內斂、直覺敏銳，善於體察他人情緒。",
           "en": "Yin Water",
           "id": "Air Yin"},
}

MAJOR_STAR_BLURB = {
    "紫微": {"zh": "領導格局，重視地位與尊嚴，天生带著一種「帝王氣」，喜歡掌控大局。",
             "en": "A leadership pattern — values status and dignity, carries a natural \"commanding presence,\" likes being in control of the big picture.",
             "id": "Pola kepemimpinan — menghargai status dan martabat, memiliki \"aura pemimpin\" alami, suka mengendalikan gambaran besar."},
    "天機": {"zh": "腦筋轉得快，善謀略、點子多，但也容易多想，情緒隨思緒起伏。",
             "en": "Strategist star",
             "id": "Bintang Strategi"},
    "太陽": {"zh": "光明磊落、熱心公益，付出型人格，格外在意是否「被看見」。",
             "en": "Open and upright, community-minded, a giving personality — but especially sensitive to whether that giving is \"seen.\"",
             "id": "Terbuka dan jujur, peduli pada kepentingan bersama, kepribadian yang suka memberi — tapi sangat peka apakah usahanya \"terlihat\"."},
    "武曲": {"zh": "務實剛毅，執行力強，是天生的財務與行動派，情感表達較內斂。",
             "en": "Finance star",
             "id": "Bintang Keuangan"},
    "天同": {"zh": "溫和知足，重視生活品質與情感和諧，抗壓性需要後天培養。",
             "en": "Harmony star",
             "id": "Bintang Harmoni"},
    "廉貞": {"zh": "個性複雜多面，理性與感性交織，桃花與事業心並存。",
             "en": "Integrity star",
             "id": "Bintang Integritas"},
    "天府": {"zh": "穩重厚道，善於守成與理財，是可靠的「大管家」型人物。",
             "en": "Steady and generous, good at preserving and managing resources — the reliable \"household steward\" type.",
             "id": "Stabil dan murah hati, pandai menjaga dan mengelola sumber daya — tipe \"pengurus rumah tangga\" yang dapat diandalkan."},
    "太陰": {"zh": "細膩內斂，重視家庭與內在世界，情感豐富但不輕易外露。",
             "en": "Moon star",
             "id": "Bintang Bulan"},
    "貪狼": {"zh": "多才多藝、社交手腕靈活，慾望與才華並重，人生選項多。",
             "en": "Desire star",
             "id": "Bintang Hasrat"},
    "巨門": {"zh": "口才犀利、分析力強，適合靠語言、專業吃飯，也容易因言惹議。",
             "en": "Communication star",
             "id": "Bintang Komunikasi"},
    "天相": {"zh": "溫和公正，重視形象與服務精神，是天生的協調者。",
             "en": "Minister star",
             "id": "Bintang Menteri"},
    "天梁": {"zh": "老成持重，樂於照顧他人，常扮演長輩或貴人的角色。",
             "en": "Guardian star",
             "id": "Bintang Penjaga"},
    "七殺": {"zh": "行動派、敢衝敢拚，人生起伏較大，適合開創型事業。",
             "en": "Warrior star",
             "id": "Bintang Pejuang"},
    "破軍": {"zh": "破舊立新、不安於現狀，變動與挑戰是這個格局的常態。",
             "en": "Pioneer star",
             "id": "Bintang Perintis"},
}

BUREAU_BLURB = {
    "水": {"zh": "水二局：人生節奏偏快起步，早年較早經歷變動與磨練。",
           "en": "Water Bureau (2): life tends to start at a faster pace, with change and challenge arriving earlier than usual.",
           "id": "Biro Air (2): hidup cenderung dimulai dengan lebih cepat, perubahan dan tantangan datang lebih awal dari biasanya."},
    "木": {"zh": "木三局：成長節奏中庸，穩紮穩打型的人生曲線。",
           "en": "Wood Bureau (3): a moderate growth pace — a steady, step-by-step life curve.",
           "id": "Biro Kayu (3): laju pertumbuhan sedang — kurva hidup yang stabil dan bertahap."},
    "金": {"zh": "金四局：性格中帶著一份韌性，需要時間淬鍊才能顯出光芒。",
           "en": "Metal Bureau (4): a resilient core that needs time under pressure before it truly shines.",
           "id": "Biro Logam (4): memiliki ketahanan yang perlu waktu dan tekanan sebelum benar-benar bersinar."},
    "土": {"zh": "土五局：大器晚成的格局，中年之後的發展往往更為扎實。",
           "en": "Earth Bureau (5): a \"late bloomer\" pattern — development after mid-life tends to be the most solid.",
           "id": "Biro Tanah (5): pola \"berkembang belakangan\" — perkembangan setelah usia pertengahan cenderung paling kokoh."},
    "火": {"zh": "火六局：人生起伏較為明顯，需要學習在高峰與低谷間找到平衡。",
           "en": "Fire Bureau (6): more pronounced ups and downs — the lesson is finding balance between the peaks and the valleys.",
           "id": "Biro Api (6): naik turun yang lebih terasa — pelajarannya adalah menemukan keseimbangan antara puncak dan lembah."},
}

PALACE_MEANING = {
    "命宮": {"zh": "你的核心性格與人生基調", "en": "Self (Life)", "id": "Diri (Kehidupan)"},
    "兄弟": {"zh": "手足情誼與合夥關係", "en": "Siblings", "id": "Saudara"},
    "夫妻": {"zh": "感情觀與婚姻狀態", "en": "Spouse / Partner", "id": "Pasangan"},
    "子女": {"zh": "子女緣分與創造力", "en": "Children", "id": "Anak"},
    "財帛": {"zh": "賺錢方式與金錢觀", "en": "Wealth", "id": "Kekayaan"},
    "疾厄": {"zh": "健康體質與壓力反應", "en": "Health", "id": "Kesehatan"},
    "遷移": {"zh": "外出運與人際際遇", "en": "Travel and outside world", "id": "Perjalanan dan dunia luar"},
    "交友": {"zh": "朋友圈與人脈資源", "en": "Friends and colleagues", "id": "Teman dan rekan"},
    "官祿": {"zh": "事業發展與職場定位", "en": "Career", "id": "Karier"},
    "田宅": {"zh": "不動產運與居家生活", "en": "Home and property", "id": "Rumah dan properti"},
    "福德": {"zh": "精神生活與福氣厚薄", "en": "Inner life and wellbeing", "id": "Kehidupan batin dan kesejahteraan"},
    "父母": {"zh": "與父母長輩的緣分", "en": "Parents and mentors", "id": "Orang tua dan mentor"},
}

_LABELS = {
    "your_pillars": {"zh": "你的四柱八字", "en": "Your Four Pillars (BaZi)", "id": "Empat Pilar Anda (BaZi)"},
    "day_master": {"zh": "日主（代表你自己）", "en": "Day Master (represents you)", "id": "Day Master (mewakili diri Anda)"},
    "life_palace": {"zh": "命宮", "en": "Life Palace", "id": "Istana Kehidupan"},
    "main_star_is": {"zh": "主星為", "en": "main star(s):", "id": "bintang utama:"},
    "no_main_star": {"zh": "（本宮無主星，個性受對宮及三方影響較大）", "en": "(no major star here — personality is shaped more by the opposite and triangle palaces)",
                      "id": "(tidak ada bintang utama di sini — kepribadian lebih dipengaruhi istana berhadapan dan segitiga)"},
    "ming_shen_zhu": {"zh": "命主 / 身主", "en": "Life Star / Body Star", "id": "Bintang Kehidupan / Bintang Tubuh"},
    "bureau": {"zh": "五行局", "en": "Five-Element Bureau", "id": "Biro Lima Elemen"},
    "life_star_reading": {"zh": "命宮主星解讀", "en": "Life Palace star reading", "id": "Pembacaan bintang Istana Kehidupan"},
    "no_star_generic": {"zh": "無主星", "en": "no major star", "id": "tanpa bintang utama"},
    "no_star_blurb": {"zh": "此宮由對宮及三方四正的星曜影響較大，建議合併命宮一起看。",
                       "en": "This palace is shaped more by the opposite and triangle palaces' stars — best read together with the Life Palace.",
                       "id": "Istana ini lebih dipengaruhi oleh bintang dari istana berhadapan dan segitiga — sebaiknya dibaca bersama Istana Kehidupan."},
}

# Keep the engine's Traditional Chinese names as canonical dictionary keys;
# these labels are presentation-only.
PALACE_DISPLAY = {
    "命宮": {"zh": "命宮", "en": "Self (Life)", "id": "Diri (Kehidupan)"},
    "兄弟": {"zh": "兄弟", "en": "Siblings", "id": "Saudara"},
    "夫妻": {"zh": "夫妻", "en": "Spouse / Partner", "id": "Pasangan"},
    "子女": {"zh": "子女", "en": "Children", "id": "Anak"},
    "財帛": {"zh": "財帛", "en": "Wealth", "id": "Kekayaan"},
    "疾厄": {"zh": "疾厄", "en": "Health", "id": "Kesehatan"},
    "遷移": {"zh": "遷移", "en": "Travel and outside world", "id": "Perjalanan dan dunia luar"},
    "交友": {"zh": "交友", "en": "Friends and colleagues", "id": "Teman dan rekan"},
    "官祿": {"zh": "官祿", "en": "Career", "id": "Karier"},
    "田宅": {"zh": "田宅", "en": "Home and property", "id": "Rumah dan properti"},
    "福德": {"zh": "福德", "en": "Inner life and wellbeing", "id": "Kehidupan batin dan kesejahteraan"},
    "父母": {"zh": "父母", "en": "Parents and mentors", "id": "Orang tua dan mentor"},
}

# Star names are transliterated as proper names in English and Indonesian.
STAR_DISPLAY = {
    "紫微": {"zh": "紫微", "en": "Emperor star", "id": "Bintang Kaisar"},
    "天機": {"zh": "天機", "en": "Strategist star", "id": "Bintang Strategi"},
    "太陽": {"zh": "太陽", "en": "Sun star", "id": "Bintang Matahari"},
    "武曲": {"zh": "武曲", "en": "Finance star", "id": "Bintang Keuangan"},
    "天同": {"zh": "天同", "en": "Harmony star", "id": "Bintang Harmoni"},
    "廉貞": {"zh": "廉貞", "en": "Integrity star", "id": "Bintang Integritas"},
    "天府": {"zh": "天府", "en": "Treasury star", "id": "Bintang Perbendaharaan"},
    "太陰": {"zh": "太陰", "en": "Moon star", "id": "Bintang Bulan"},
    "貪狼": {"zh": "貪狼", "en": "Desire star", "id": "Bintang Hasrat"},
    "巨門": {"zh": "巨門", "en": "Communication star", "id": "Bintang Komunikasi"},
    "天相": {"zh": "天相", "en": "Minister star", "id": "Bintang Menteri"},
    "天梁": {"zh": "天梁", "en": "Guardian star", "id": "Bintang Penjaga"},
    "七殺": {"zh": "七殺", "en": "Warrior star", "id": "Bintang Pejuang"},
    "破軍": {"zh": "破軍", "en": "Pioneer star", "id": "Bintang Perintis"},
}

STEM_DISPLAY = {
    "甲": {"zh": "甲", "en": "Yang Wood", "id": "Kayu Yang"},
    "乙": {"zh": "乙", "en": "Yin Wood", "id": "Kayu Yin"},
    "丙": {"zh": "丙", "en": "Yang Fire", "id": "Api Yang"},
    "丁": {"zh": "丁", "en": "Yin Fire", "id": "Api Yin"},
    "戊": {"zh": "戊", "en": "Yang Earth", "id": "Tanah Yang"},
    "己": {"zh": "己", "en": "Yin Earth", "id": "Tanah Yin"},
    "庚": {"zh": "庚", "en": "Yang Metal", "id": "Logam Yang"},
    "辛": {"zh": "辛", "en": "Yin Metal", "id": "Logam Yin"},
    "壬": {"zh": "壬", "en": "Yang Water", "id": "Air Yang"},
    "癸": {"zh": "癸", "en": "Yin Water", "id": "Air Yin"},
}
BRANCH_DISPLAY = {
    "子": {"zh": "子", "en": "Rat", "id": "Tikus"},
    "丑": {"zh": "丑", "en": "Ox", "id": "Kerbau"},
    "寅": {"zh": "寅", "en": "Tiger", "id": "Harimau"},
    "卯": {"zh": "卯", "en": "Rabbit", "id": "Kelinci"},
    "辰": {"zh": "辰", "en": "Dragon", "id": "Naga"},
    "巳": {"zh": "巳", "en": "Snake", "id": "Ular"},
    "午": {"zh": "午", "en": "Horse", "id": "Kuda"},
    "未": {"zh": "未", "en": "Goat", "id": "Kambing"},
    "申": {"zh": "申", "en": "Monkey", "id": "Monyet"},
    "酉": {"zh": "酉", "en": "Rooster", "id": "Ayam jantan"},
    "戌": {"zh": "戌", "en": "Dog", "id": "Anjing"},
    "亥": {"zh": "亥", "en": "Pig", "id": "Babi"},
}
ELEMENT_DISPLAY = {
    "木": {"zh": "木", "en": "Wood", "id": "Kayu"},
    "金": {"zh": "金", "en": "Metal", "id": "Logam"},
    "水": {"zh": "水", "en": "Water", "id": "Air"},
    "火": {"zh": "火", "en": "Fire", "id": "Api"},
    "土": {"zh": "土", "en": "Earth", "id": "Tanah"},
}


def _localized(mapping, value, lang):
    return mapping.get(value, {}).get(lang, mapping.get(value, {}).get("zh", value))


def display_palace(value, lang):
    return _localized(PALACE_DISPLAY, value, lang)


def display_star(value, lang):
    return _localized(STAR_DISPLAY, value, lang)


def display_stem_branch(stem, branch, lang):
    if lang == "zh":
        return f"{stem}{branch}"
    return f"{_localized(STEM_DISPLAY, stem, lang)}-{_localized(BRANCH_DISPLAY, branch, lang)}"


def _display_pillar(value, lang):
    if lang == "zh":
        return value
    if len(value) >= 2 and value[0] in STEM_DISPLAY and value[1] in BRANCH_DISPLAY:
        return display_stem_branch(value[0], value[1], lang)
    return _localized(STEM_DISPLAY, value, lang)


def _display_bureau(ziwei, lang):
    if lang == "zh":
        return ziwei.bureau_name
    element = _localized(ELEMENT_DISPLAY, ziwei.bureau_element, lang)
    label = "Bureau" if lang == "en" else "Biro"
    return f"{element} {label} ({ziwei.bureau_number})"


def free_tier_summary(bazi_pillars, day_master, ziwei, lang="zh"):
    life_row = ziwei.palace_table()[0]
    separator = "、" if lang == "zh" else ", "
    star_text = separator.join(display_star(s, lang) for s in life_row["stars"]) if life_row["stars"] else _LABELS["no_main_star"][lang]
    day_stem = bazi_pillars["day"][0]
    L = {k: v[lang] for k, v in _LABELS.items()}
    colon = "：" if lang == "zh" else ": "
    dash = " — "
    lines = [
        f"**{L['your_pillars']}**{colon}{' '.join(_display_pillar(bazi_pillars[k], lang) for k in ('year', 'month', 'day', 'hour'))}",
        f"**{L['day_master']}**{colon}{_localized(STEM_DISPLAY, day_stem, lang)}{dash}{DAY_MASTER_BLURB.get(day_stem, {}).get(lang, '')}",
        f"**{L['life_palace']}**{colon}{display_stem_branch(life_row['stem'], life_row['branch'], lang)}, {L['main_star_is']} {star_text}",
        f"**{L['ming_shen_zhu']}**{colon}{display_star(ziwei.ming_zhu, lang)} / {display_star(ziwei.shen_zhu, lang)}",
        f"**{L['bureau']}**{colon}{_display_bureau(ziwei, lang)}{dash}{BUREAU_BLURB.get(ziwei.bureau_element, {}).get(lang, '')}",
    ]
    if life_row["stars"]:
        lines.append(f"**{L['life_star_reading']}**：" + " ".join(MAJOR_STAR_BLURB.get(s, {}).get(lang, "") for s in life_row["stars"]))
    return "\n\n".join(lines)


def paid_tier_report(ziwei, current_year=None, lang="zh"):
    rows = ziwei.palace_table()
    out = []
    for row in rows:
        star_separator = "、" if lang == "zh" else ", "
        stars = star_separator.join(display_star(s, lang) for s in row["stars"]) if row["stars"] else _LABELS["no_star_generic"][lang]
        blurb = " ".join(MAJOR_STAR_BLURB.get(s, {}).get(lang, "") for s in row["stars"]) or _LABELS["no_star_blurb"][lang]
        body_tag = ""
        if row["is_body_palace"]:
            body_tag = {"zh": "（身宮）", "en": " (Body Palace)", "id": " (Istana Tubuh)"}[lang]
        d_start, d_end = row["decade"]["range"]
        suffix = "歲" if lang == "zh" else "" if lang == "en" else " tahun"
        out.append({
            "palace": display_palace(row["palace"], lang) + body_tag,
            "meaning": PALACE_MEANING.get(row["palace"], {}).get(lang, ""),
            "stem_branch": display_stem_branch(row["stem"], row["branch"], lang),
            "stars": stars,
            "blurb": blurb,
            "decade_range": f"{d_start}–{d_end}{suffix}",
        })
    current_palace = ziwei.current_year_palace(current_year) if current_year else None
    return out, current_palace
