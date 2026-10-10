"""
glossary.py - meaning-based translations for Zi Wei Dou Shu / BaZi terms.

Rule: users see the MEANING (en / id), never the pinyin sound.
Pinyin + Chinese appear only when show_traditional=True.

Quick use:
    from glossary import term, translate_text
    term("天同", "en")                      -> "Harmony star"
    term("天同", "id")                      -> "Bintang Harmoni"
    term("天同", "en", show_traditional=True) -> "Harmony star (Tian Tong 天同)"
    translate_text("命宮：官祿宮，主星：天同", "en")

Run `python glossary.py` to execute the built-in self-test.
Entries with review=True are proposals that a native speaker should check.
"""
import logging
import re

log = logging.getLogger("glossary")


def E(key, zh, en, idn, pinyin, meaning, aliases=(), review=False):
    return {
        "key": key, "zh": zh, "en": en, "id": idn, "pinyin": pinyin,
        "meaning": meaning, "aliases": list(aliases), "review": review,
    }


ENTRIES = [
    # ---- Main stars ----
    E("star.zi_wei", "紫微", "Emperor star", "Bintang Kaisar", "Zi Wei", "Leadership, status, authority"),
    E("star.tian_ji", "天機", "Strategist star", "Bintang Strategi", "Tian Ji", "Planning, adaptability", ["天机"]),
    E("star.tai_yang", "太陽", "Sun star", "Bintang Matahari", "Tai Yang", "Visibility, generosity", ["太阳"]),
    E("star.wu_qu", "武曲", "Finance star", "Bintang Keuangan", "Wu Qu", "Money, discipline"),
    E("star.tian_tong", "天同", "Harmony star", "Bintang Harmoni", "Tian Tong", "Comfort, ease, contentment"),
    E("star.lian_zhen", "廉貞", "Integrity star", "Bintang Integritas", "Lian Zhen", "Passion, principles", ["廉贞"]),
    E("star.tian_fu", "天府", "Treasury star", "Bintang Perbendaharaan", "Tian Fu", "Stability, resources"),
    E("star.tai_yin", "太陰", "Moon star", "Bintang Bulan", "Tai Yin", "Sensitivity, savings", ["太阴"]),
    E("star.tan_lang", "貪狼", "Desire star", "Bintang Hasrat", "Tan Lang", "Ambition, charm", ["贪狼"]),
    E("star.ju_men", "巨門", "Communication star", "Bintang Komunikasi", "Ju Men", "Speech, analysis, disputes", ["巨门"]),
    E("star.tian_xiang", "天相", "Minister star", "Bintang Menteri", "Tian Xiang", "Support, service"),
    E("star.tian_liang", "天梁", "Guardian star", "Bintang Penjaga", "Tian Liang", "Protection, mentorship"),
    E("star.qi_sha", "七殺", "Warrior star", "Bintang Pejuang", "Qi Sha", "Courage, bold change", ["七杀"]),
    E("star.po_jun", "破軍", "Pioneer star", "Bintang Perintis", "Po Jun", "Breaking old patterns, renewal", ["破军"]),
    # Stars that appear as Life ruler / Body ruler (proposals)
    E("star.lu_cun", "祿存", "Wealth-keeper star", "Bintang Penjaga Rezeki", "Lu Cun", "Steady resources", ["禄存"], True),
    E("star.wen_qu", "文曲", "Arts star", "Bintang Seni", "Wen Qu", "Talent, expression", [], True),
    E("star.wen_chang", "文昌", "Scholar star", "Bintang Cendekia", "Wen Chang", "Learning, writing, exams", [], True),
    E("star.huo_xing", "火星", "Fire star", "Bintang Api", "Huo Xing", "Sudden energy, urgency", [], True),

    # ---- 12 palaces ----
    E("palace.ming", "命宮", "Self (Life)", "Diri (Kehidupan)", "Ming", "You: character and direction", ["命宫"]),
    E("palace.siblings", "兄弟", "Siblings", "Saudara", "Xiong Di", "Siblings and close peers"),
    E("palace.spouse", "夫妻", "Spouse / Partner", "Pasangan", "Fu Qi", "Marriage and close partnership"),
    E("palace.children", "子女", "Children", "Anak", "Zi Nu", "Children and creative output"),
    E("palace.wealth", "財帛", "Wealth", "Kekayaan", "Cai Bo", "Income and money habits", ["财帛"]),
    E("palace.health", "疾厄", "Health", "Kesehatan", "Ji E", "Health and vulnerabilities"),
    E("palace.travel", "遷移", "Travel and outside world", "Perjalanan dan dunia luar", "Qian Yi", "Travel, moves, how you fare outside", ["迁移"]),
    E("palace.friends", "交友", "Friends and colleagues", "Teman dan rekan", "Jiao You", "Friends, colleagues, social circle", ["僕役", "仆役"]),
    E("palace.career", "官祿", "Career", "Karier", "Guan Lu", "Work and achievement", ["官禄"]),
    E("palace.property", "田宅", "Home and property", "Rumah dan properti", "Tian Zhai", "Home, property, family base"),
    E("palace.fortune", "福德", "Inner life and wellbeing", "Kehidupan batin dan kesejahteraan", "Fu De", "Mindset, enjoyment, inner peace"),
    E("palace.parents", "父母", "Parents and mentors", "Orang tua dan mentor", "Fu Mu", "Parents, mentors, authority figures"),

    # ---- Four Transformations ----
    E("mutagen.lu", "化祿", "Prosperity", "Kemakmuran", "Hua Lu", "Gain, benefit, resources flowing in", ["化禄"]),
    E("mutagen.quan", "化權", "Authority", "Otoritas", "Hua Quan", "Control, drive, taking charge", ["化权"]),
    E("mutagen.ke", "化科", "Recognition", "Pengakuan", "Hua Ke", "Reputation, support, smooth outcomes"),
    E("mutagen.ji", "化忌", "Obstruction", "Hambatan", "Hua Ji", "Friction or worry that needs attention"),

    # ---- Element bureaus ----
    E("bureau.water2", "水二局", "Water 2", "Air 2", "Shui Er Ju", "Water element type, decade starts at age 2"),
    E("bureau.wood3", "木三局", "Wood 3", "Kayu 3", "Mu San Ju", "Wood element type, decade starts at age 3"),
    E("bureau.metal4", "金四局", "Metal 4", "Logam 4", "Jin Si Ju", "Metal element type, decade starts at age 4"),
    E("bureau.earth5", "土五局", "Earth 5", "Tanah 5", "Tu Wu Ju", "Earth element type, decade starts at age 5"),
    E("bureau.fire6", "火六局", "Fire 6", "Api 6", "Huo Liu Ju", "Fire element type, decade starts at age 6"),

    # ---- Star brightness (single characters: used by term() only) ----
    E("bright.miao", "廟", "Radiant", "Bersinar", "Miao", "Star at its strongest", ["庙"]),
    E("bright.wang", "旺", "Strong", "Kuat", "Wang", "Star in good strength"),
    E("bright.ping", "平", "Neutral", "Netral", "Ping", "Star with average strength"),
    E("bright.xian", "陷", "Weak", "Lemah", "Xian", "Star with reduced strength"),

    # ---- Layers and concepts ----
    E("layer.natal", "本命盤", "Birth chart", "Bagan kelahiran", "Ben Ming Pan", "Your fixed chart", ["本命盘"]),
    E("layer.decade", "大限", "10-year cycle", "Siklus 10 tahun", "Da Xian", "Current ten-year chapter of life"),
    E("layer.year", "流年", "Yearly cycle", "Siklus tahunan", "Liu Nian", "Theme of a given year"),
    E("layer.month", "流月", "Monthly cycle", "Siklus bulanan", "Liu Yue", "Theme of a given month"),
    E("layer.day", "流日", "Daily cycle", "Siklus harian", "Liu Ri", "Theme of a given day"),
    E("concept.four_palace", "三方四正", "Four-palace group", "Kelompok empat istana", "San Fang Si Zheng",
      "A palace read together with its opposite and two supporting palaces"),
    E("concept.opposite", "對宮", "Opposite palace (outside influence)", "Istana seberang (pengaruh luar)", "Dui Gong",
      "The palace across the chart that pushes on yours", ["对宫"]),
    E("concept.trine", "三合宮", "Supporting palaces", "Istana pendukung", "San He Gong",
      "The two palaces that back up the palace you read", ["三合宫"]),
    E("concept.four_transformations", "四化", "Four Transformations", "Empat Transformasi", "Si Hua",
      "Prosperity, Authority, Recognition, Obstruction"),
    E("concept.bureau", "五行局", "Element type", "Tipe unsur", "Wu Xing Ju", "Element group that sets the decade timing"),
    E("concept.malefic", "煞星", "Challenging stars", "Bintang penantang", "Sha Xing", "Stars that add friction", ["煞曜"]),
    E("concept.body_palace", "身宮", "Body palace", "Istana tubuh", "Shen Gong", "Secondary focus of the chart", ["身宫"]),
    E("concept.life_ruler", "命主", "Life ruler", "Penguasa kehidupan", "Ming Zhu", "Star that rules your life palace"),
    E("concept.body_ruler", "身主", "Body ruler", "Penguasa tubuh", "Shen Zhu", "Star that rules your body palace"),
    E("concept.day_master", "日主", "Day Master", "Day Master (unsur diri)", "Ri Zhu", "Core element of your BaZi chart"),
    E("concept.four_pillars", "四柱八字", "Four Pillars (BaZi)", "Empat Pilar (BaZi)", "Si Zhu Ba Zi", "Year, month, day and hour pillars"),
    E("concept.twelve_palaces", "十二宮", "12 palaces", "12 istana", "Shi Er Gong", "The twelve life areas", ["十二宫"]),
    E("concept.major_stars", "主星", "major stars", "bintang utama", "Zhu Xing", "The main stars in a palace"),
    E("concept.no_major_star", "無主星", "no major star", "tanpa bintang utama", "Wu Zhu Xing", "Empty palace", ["无主星"]),
    E("concept.auxiliary", "輔星", "auxiliary stars", "bintang tambahan", "Fu Xing", "Supporting stars", ["辅星"]),
]

# ---- BaZi stems and branches (used by translate_pillar) ----
STEMS = {
    "甲": ("Yang Wood", "Kayu Yang"), "乙": ("Yin Wood", "Kayu Yin"),
    "丙": ("Yang Fire", "Api Yang"), "丁": ("Yin Fire", "Api Yin"),
    "戊": ("Yang Earth", "Tanah Yang"), "己": ("Yin Earth", "Tanah Yin"),
    "庚": ("Yang Metal", "Logam Yang"), "辛": ("Yin Metal", "Logam Yin"),
    "壬": ("Yang Water", "Air Yang"), "癸": ("Yin Water", "Air Yin"),
}
BRANCHES = {
    "子": ("Rat", "Tikus"), "丑": ("Ox", "Kerbau"), "寅": ("Tiger", "Harimau"),
    "卯": ("Rabbit", "Kelinci"), "辰": ("Dragon", "Naga"), "巳": ("Snake", "Ular"),
    "午": ("Horse", "Kuda"), "未": ("Goat", "Kambing"), "申": ("Monkey", "Monyet"),
    "酉": ("Rooster", "Ayam jantan"), "戌": ("Dog", "Anjing"), "亥": ("Pig", "Babi"),
}

# ---- lookup structures ----
_INDEX = {}
for _e in ENTRIES:
    for _k in [_e["key"], _e["zh"], *_e["aliases"]]:
        _INDEX.setdefault(_k, _e)

# multi-character Chinese terms only (single characters are too risky to replace in free text)
_MULTI = sorted([k for k in _INDEX if len(k) >= 2 and re.search(r"[\u4e00-\u9fff]", k)],
                key=len, reverse=True)

# multi-word pinyin only (single words like "Wang" could clash with normal text)
PINYIN_SET = {e["pinyin"] for e in ENTRIES if " " in e["pinyin"]}

_STEM_CHARS = "".join(STEMS)
_BRANCH_CHARS = "".join(BRANCHES)
_PILLAR = r"[%s][%s]" % (_STEM_CHARS, _BRANCH_CHARS)
_PATTERN = re.compile("|".join([re.escape(k) for k in _MULTI] + [_PILLAR]))
_DAY_MASTER = re.compile(r"(日主[:：]\s*)([%s])" % _STEM_CHARS)

_PUNCT = {ord("："): ": ", ord("，"): ", ", ord("、"): ", ", ord("（"): " (",
          ord("）"): ")", ord("／"): " / ", ord("。"): ". ", ord("；"): "; "}
_YEARS = {"en": " yrs", "id": " thn"}


def _lang(lang):
    return lang if lang in ("zh", "en", "id") else "en"


def term(key_or_zh, lang="en", show_traditional=False):
    """Return the label in `lang`. Accepts a key, the Chinese term, or an alias."""
    e = _INDEX.get(key_or_zh)
    if e is None:
        log.warning("glossary: unknown term %r", key_or_zh)
        return key_or_zh
    lang = _lang(lang)
    if lang == "zh":
        return e["zh"]
    label = e[lang]
    if show_traditional:
        return "%s (%s %s)" % (label, e["pinyin"], e["zh"])
    return label


def translate_pillar(text, lang="en", show_traditional=False):
    """Translate stem+branch characters, e.g. 甲子 -> 'Yang Wood Rat'."""
    lang = _lang(lang)
    if lang == "zh":
        return text
    idx = 0 if lang == "en" else 1
    parts = []
    for ch in text:
        if ch in STEMS:
            parts.append(STEMS[ch][idx])
        elif ch in BRANCHES:
            parts.append(BRANCHES[ch][idx])
        else:
            parts.append(ch)
    out = " ".join(parts)
    return "%s (%s)" % (out, text) if show_traditional else out


def translate_text(text, lang="en", show_traditional=False):
    """Replace every known Chinese term in a string with its meaning-based label.
    Also converts Chinese punctuation, 歲, and stem/branch pillars.
    For lang='zh' the text is returned unchanged."""
    lang = _lang(lang)
    if lang == "zh" or not text:
        return text
    idx = 0 if lang == "en" else 1

    text = _DAY_MASTER.sub(lambda m: m.group(1) + STEMS[m.group(2)][idx], text)

    def repl(m):
        s = m.group(0)
        if s in _INDEX:
            return term(s, lang, show_traditional)
        return translate_pillar(s, lang, show_traditional)

    text = _PATTERN.sub(repl, text)
    text = re.sub(r"(\d+)\s*[歲岁]", lambda m: m.group(1) + _YEARS[lang], text)
    text = text.translate(_PUNCT)
    text = re.sub(r" {2,}", " ", text)
    if not show_traditional:
        left = leftover_chinese(text)
        if left:
            log.warning("glossary: untranslated Chinese left: %s", "".join(sorted(left)))
    return text


def leftover_chinese(text):
    """Set of Chinese characters still present in text."""
    return set(re.findall(r"[\u4e00-\u9fff]", text or ""))


def find_pinyin(text):
    """Known multi-word pinyin strings found in text (case-insensitive)."""
    low = (text or "").lower()
    return sorted(p for p in PINYIN_SET if p.lower() in low)


if __name__ == "__main__":
    # ---- self-test ----
    assert term("天同", "en") == "Harmony star"
    assert term("天同", "id") == "Bintang Harmoni"
    assert term("廉贞", "en") == "Integrity star"          # simplified alias
    assert term("僕役", "en") == term("仆役", "en") == "Friends and colleagues"
    assert term("star.zi_wei", "en") == "Emperor star"
    assert term("天同", "en", True) == "Harmony star (Tian Tong 天同)"
    assert term("not-a-term", "en") == "not-a-term"         # unknown: no crash

    sample = "十二宮：\n- 命宮（身宮）：甲子，主星：天同、貪狼，大限：4-13歲\n五行局：水二局\n日主：甲\n命主／身主：貪狼 / 天相"
    for lg in ("en", "id"):
        out = translate_text(sample, lg)
        assert not leftover_chinese(out), (lg, leftover_chinese(out))
        assert not find_pinyin(out), (lg, find_pinyin(out))
        print("---", lg, "---")
        print(out)
    print("\nAll glossary self-tests passed.")
