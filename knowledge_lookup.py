"""Look up star definitions from data/reference_stars.json for a given chart."""

import json
import os


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


def _load():
    global _CACHE
    if _CACHE is None:
        with open(_PATH, encoding="utf-8") as f:
            _CACHE = json.load(f)
    return _CACHE


def lookup_star_definitions(zw, max_stars=3):
    """Return definitions for chart stars, prioritizing the Life Palace."""
    if max_stars <= 0:
        return []

    all_defs = _load()
    by_name = {definition["star_name_zh"]: definition for definition in all_defs}
    rows = zw.palace_table()
    life_rows = [row for row in rows if row["palace"] == "命宮"]
    other_rows = [row for row in rows if row["palace"] != "命宮"]
    seen = []

    for row in life_rows + other_rows:
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


def format_star_definitions(defs):
    """Render star definitions as text to append to chart_context."""
    if not defs:
        return ""
    lines = ["", "【星曜定義 / Star definitions】"]
    for definition in defs:
        lines.append(
            f"- {definition['star_name_zh']} ({definition['star_name_en']}, "
            f"{definition['pinyin']}) — {definition['element']}, associated with "
            f"{definition['associated_palace']}"
        )
        lines.append(f"  Brief: {definition['description']['en']}")
        classical_expansion = definition.get("classical_expansion")
        if classical_expansion:
            lines.append(f"  Classical: {classical_expansion['classical_text_zh']}")
            lines.append(
                f"  Translation: {classical_expansion['modern_translation_en']}"
            )
            if classical_expansion.get("practical_advice"):
                lines.append("  Advice:")
                for advice in classical_expansion["practical_advice"]:
                    lines.append(f"    - {advice}")
            if classical_expansion.get("palace_notes"):
                for palace, note in classical_expansion["palace_notes"].items():
                    lines.append(f"  In {palace} Palace: {note}")
    return "\n".join(lines)
