"""Look up star definitions from data/reference_stars.json for a given chart."""

import json
import os
import re


_PATH = os.path.join(os.path.dirname(__file__), "data", "reference_stars.json")
_CACHE = None
_TRADITIONAL_TO_SIMPLIFIED = {
    "天機": "天机",
    "太陽": "太阳",
    "廉貞": "廉贞",
    "太陰": "太阴",
    "貪狼": "贪狼",
    "巨門": "巨门",
    "七殺": "七杀",
    "破軍": "破军",
}
_PALACE_QUESTION_TERMS = (
    ("官祿", (
        "career", "job", "work", "職業", "事业", "事業", "工作", "升職", "升职",
        "karier", "pekerjaan", "profesi",
    )),
    ("財帛", (
        "wealth", "money", "finance", "financial", "財", "财", "財務", "财务",
        "金錢", "金钱", "收入", "uang", "keuangan", "penghasilan",
    )),
    ("夫妻", (
        "relationship", "partner", "marriage", "love", "dating", "感情", "伴侶",
        "伴侣", "婚姻", "戀愛", "恋爱", "hubungan", "pasangan", "pernikahan",
    )),
    ("疾厄", (
        "health", "illness", "medical", "健康", "疾病", "身體", "身体",
        "kesehatan", "penyakit",
    )),
    ("遷移", (
        "travel", "move", "relocation", "出行", "旅行", "搬家", "遷移", "迁移",
        "perjalanan", "pindah",
    )),
    ("田宅", (
        "property", "home", "house", "real estate", "房屋", "房產", "房产", "田宅",
        "rumah", "properti",
    )),
    ("子女", ("children", "child", "子女", "孩子", "anak")),
    ("父母", (
        "parents", "parent", "father", "mother", "父母", "父親", "父亲", "母親",
        "母亲", "orang tua", "ayah", "ibu",
    )),
    ("兄弟", (
        "siblings", "brother", "sister", "兄弟", "姊妹", "姐妹", "saudara",
    )),
    ("交友", (
        "friends", "friend", "network", "social", "朋友", "人際", "人际", "交友",
        "teman", "jaringan",
    )),
    ("福德", (
        "spiritual", "wellbeing", "happiness", "inner life", "福德", "精神", "心境",
        "batin", "kesejahteraan",
    )),
    ("命宮", (
        "personality", "self", "identity", "命宮", "命宫", "個性", "个性", "自我",
        "kepribadian",
    )),
)


def _load():
    global _CACHE
    if _CACHE is None:
        with open(_PATH, encoding="utf-8") as f:
            _CACHE = json.load(f)
    return _CACHE


def _question_term_position(question, term):
    term = term.casefold()
    if re.search(r"[a-z]", term, re.IGNORECASE):
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        match = re.search(pattern, question)
        return match.start() if match else None
    position = question.find(term)
    return position if position >= 0 else None


def _question_palaces(question):
    question = (question or "").casefold()
    matches = []
    for palace, terms in _PALACE_QUESTION_TERMS:
        positions = []
        for term in terms:
            position = _question_term_position(question, term)
            if position is not None:
                positions.append(position)
        if positions:
            matches.append((min(positions), palace))
    return [palace for _, palace in sorted(matches)]


def lookup_star_definitions(zw, max_stars=3, question=None):
    """Return definitions for chart stars, prioritizing the question's palace."""
    if max_stars <= 0:
        return []

    all_defs = _load()
    by_name = {definition["star_name_zh"]: definition for definition in all_defs}
    rows = zw.palace_table()
    question_palaces = _question_palaces(question)
    prioritized_rows = [
        row for palace in question_palaces
        for row in rows if row["palace"] == palace
    ]
    life_rows = [row for row in rows if row["palace"] == "命宮"]
    other_rows = [
        row for row in rows
        if row["palace"] != "命宮" and row not in prioritized_rows
    ]
    ordered_rows = prioritized_rows + [
        row for row in life_rows if row not in prioritized_rows
    ] + other_rows
    seen = []

    for row in ordered_rows:
        for star in row["stars"]:
            normalized = _TRADITIONAL_TO_SIMPLIFIED.get(star, star)
            for candidate in (normalized, normalized + "星"):
                if candidate in by_name and candidate not in seen:
                    seen.append(candidate)
                    break
            if len(seen) >= max_stars:
                break
        if len(seen) >= max_stars:
            break

    return [by_name[name] for name in seen]


def format_star_definitions(defs, lang="zh"):
    """Render definitions in Chinese or English-language form for the model."""
    if not defs:
        return ""
    lang = lang if lang in ("zh", "en", "id") else "zh"
    header = "【星曜定義 / Star definitions】" if lang == "zh" else "Star definitions:"
    lines = ["", header]
    for definition in defs:
        if lang == "zh":
            lines.append(
                f"- {definition['star_name_zh']} ({definition['star_name_en']}, "
                f"{definition['pinyin']}) — {definition['element']}, associated with "
                f"{definition['associated_palace']}"
            )
        else:
            element = definition["element"].split(" ", 1)[-1]
            associated_palace = definition["associated_palace"].split(" / ")[-1]
            lines.append(
                f"- {definition['star_name_en']} — {element}, associated with "
                f"{associated_palace}"
            )
        lines.append(f"  Brief: {definition['description']['en']}")
        classical_expansion = definition.get("classical_expansion")
        if classical_expansion:
            if lang == "zh":
                lines.append(
                    f"  Classical: {classical_expansion['classical_text_zh']}"
                )
            provenance = classical_expansion.get("provenance") or {}
            if provenance.get("verification_status") != "verified":
                if lang == "zh":
                    lines.append("  來源尚未核實；此段內容應視為暫定參考。")
                elif lang == "id":
                    lines.append(
                        "  Sumber belum diverifikasi; anggap uraian ini sebagai "
                        "referensi sementara."
                    )
                else:
                    lines.append(
                        "  Provenance is unverified; treat this expansion as provisional."
                    )
            lines.append(
                f"  {'現代摘要' if lang == 'zh' else 'Modern summary'}: "
                f"{classical_expansion['modern_summary_en']}"
            )
            if lang == "zh":
                lines.append("  解讀提示：此為傳統象徵性說法，並非確定預測或醫療建議。")
            elif lang == "id":
                lines.append(
                    "  Note: Interpretasi simbolis tradisional, bukan prediksi pasti "
                    "atau nasihat medis."
                )
            else:
                lines.append(
                    "  Note: Traditional symbolic interpretation, not a factual "
                    "prediction or medical advice."
                )
            if classical_expansion.get("practical_advice"):
                lines.append("  Advice:")
                for advice in classical_expansion["practical_advice"]:
                    lines.append(f"    - {advice}")
            if classical_expansion.get("palace_notes"):
                for palace, note in classical_expansion["palace_notes"].items():
                    lines.append(f"  In {palace} Palace: {note}")
    return "\n".join(lines)
