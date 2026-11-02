"""Look up star definitions from data/reference_stars.json for a given chart."""

import json
import os
import re
from urllib.parse import quote


_PATH = os.path.join(os.path.dirname(__file__), "data", "reference_stars.json")
_PATTERNS_PATH = os.path.join(
    os.path.dirname(__file__), "data", "reference_patterns.json"
)
_CACHE = None
_PATTERN_CACHE = None
_TRADITIONAL_TO_SIMPLIFIED = {
    "左輔": "左辅",
    "天機": "天机",
    "太陽": "太阳",
    "廉貞": "廉贞",
    "太陰": "太阴",
    "貪狼": "贪狼",
    "巨門": "巨门",
    "七殺": "七杀",
    "破軍": "破军",
    "右弼": "右弼",
    "文昌": "文昌",
    "文曲": "文曲",
    "天魁": "天魁",
    "天鉞": "天钺",
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


def _load_patterns():
    global _PATTERN_CACHE
    if _PATTERN_CACHE is None:
        with open(_PATTERNS_PATH, encoding="utf-8") as f:
            _PATTERN_CACHE = json.load(f)
    return _PATTERN_CACHE


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


def _normalized_star_name(name):
    return _TRADITIONAL_TO_SIMPLIFIED.get(name, name)


def _pattern_branch_matches(pattern, rows, candidate_rows):
    extra_conditions = pattern["trigger"].get("extra_conditions", "")
    extra_conditions = re.sub(
        r"[子丑寅卯辰巳午未申酉戌亥]年", "", extra_conditions
    )
    branches = set(re.findall(r"[子丑寅卯辰巳午未申酉戌亥]", extra_conditions))
    if not branches:
        return True

    if "命" in extra_conditions or "life palace" in extra_conditions.casefold():
        relevant_rows = [row for row in rows if row["palace"] == "命宮"]
    else:
        relevant_rows = [
            row for row in candidate_rows
            if any(
                _normalized_star_name(star)
                in {
                    _normalized_star_name(name)
                    for name in pattern["trigger"]["required_stars"]
                }
                for star in row["stars"]
            )
        ]
    return bool(relevant_rows) and all(row["branch"] in branches for row in relevant_rows)


def _pattern_matches(pattern, rows):
    trigger = pattern["trigger"]
    condition = trigger["condition"]
    if condition == "ambiguous":
        return False

    palace_names = trigger.get("palaces") or []
    required_stars = {
        _normalized_star_name(name) for name in trigger["required_stars"]
    }

    if condition == "flanking":
        target_palace = palace_names[0] if palace_names else "命宮"
        target_index = next(
            (index for index, row in enumerate(rows)
             if row["palace"] == target_palace),
            None,
        )
        if target_index is None:
            return False
        adjacent_rows = (
            rows[(target_index - 1) % len(rows)],
            rows[(target_index + 1) % len(rows)],
        )
        present_stars = {
            _normalized_star_name(star)
            for row in adjacent_rows
            for star in row["stars"]
        }
        return required_stars.issubset(present_stars)

    if condition != "specific_arrangement":
        return False

    candidate_rows = [
        row for row in rows
        if not palace_names or row["palace"] in palace_names
    ]
    present_stars = {
        _normalized_star_name(star)
        for row in candidate_rows
        for star in row["stars"]
    }
    if not required_stars.issubset(present_stars):
        return False

    return _pattern_branch_matches(pattern, rows, candidate_rows)


def lookup_patterns(zw, question=None, max_patterns=3):
    """Return chart patterns with non-ambiguous triggers, prioritized by topic."""
    if max_patterns <= 0:
        return []

    rows = zw.palace_table()
    question_palaces = _question_palaces(question)
    matched = [
        (index, pattern)
        for index, pattern in enumerate(_load_patterns())
        if _pattern_matches(pattern, rows)
    ]

    def priority(item):
        _, pattern = item
        palace_names = pattern["trigger"].get("palaces") or []
        question_match = any(palace in question_palaces for palace in palace_names)
        if "命宮" in palace_names:
            palace_priority = 0
        elif palace_names:
            palace_priority = 1
        else:
            palace_priority = 2
        return (not question_match, palace_priority, item[0])

    matched.sort(key=priority)
    return [pattern for _, pattern in matched[:max_patterns]]


def format_patterns(patterns, lang="zh"):
    """Render matched patterns for the model context."""
    if not patterns:
        return ""
    lines = [""]
    if lang == "zh":
        lines.append("【命盤格局 / Chart patterns】")
    else:
        lines.append("Chart patterns:")
    for pattern in patterns:
        if lang == "zh":
            lines.append(f"- {pattern['name_zh']} ({pattern['name_en']})")
            if pattern.get("classical_text_zh"):
                lines.append(f"  Classical: {pattern['classical_text_zh']}")
            lines.append(f"  Meaning: {pattern['modern_summary_en']}")
        else:
            lines.append(f"- {pattern['name_en']}")
            lines.append(f"  Source Meaning: {pattern['modern_summary_en']}")
        lines.append("  Advice: " + " | ".join(pattern["practical_advice"]))
        provenance = pattern.get("provenance") or {}
        source = pattern.get("classical_source") or "Source not recorded"
        if lang != "zh":
            source = source.replace(
                "《紫微斗數全書》卷一、卷三",
                "Zi Wei Dou Shu Quan Shu, Volumes I and III",
            ).replace(
                "《紫微斗數全書》卷一",
                "Zi Wei Dou Shu Quan Shu, Volume I",
            ).replace(
                "《紫微斗數全書》卷二",
                "Zi Wei Dou Shu Quan Shu, Volume II",
            ).replace(
                "《紫微斗數全書》卷三",
                "Zi Wei Dou Shu Quan Shu, Volume III",
            ).replace(
                " (Wikisource transcription; edition not independently verified)",
                "",
            )
        lines.append(f"  Source: {source}")
        status = provenance.get("verification_status")
        if status == "transcription_located_edition_unverified":
            if lang == "zh":
                lines.append("  來源狀態：已找到文字轉錄本；印刷版本尚未獨立核實。")
            else:
                lines.append(
                    "  Source status: text transcription located; print edition "
                    "not independently verified."
                )
        elif status == "verified":
            lines.append("  Source status: marked verified in the dataset.")
        else:
            lines.append("  Source status: missing or unknown; do not treat as verified.")
        if provenance.get("url"):
            source_url = quote(
                provenance["url"], safe=":/?#[]@!$&'()*+,;=%"
            )
            lines.append(f"  Source URL: {source_url}")
    return "\n".join(lines)


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
            source_url = provenance.get("url")
            if source_url:
                source_title = (
                    classical_expansion.get("classical_source")
                    if lang == "zh"
                    else "Zi Wei Dou Shu Quan Shu, Volume I (claimed source)"
                )
                lines.append(f"  Source: {source_title}")
                source_url = quote(source_url, safe=":/?#[]@!$&'()*+,;=%")
                lines.append(f"  Source URL: {source_url}")
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
