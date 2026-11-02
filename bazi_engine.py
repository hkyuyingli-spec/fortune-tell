"""Simplified BaZi analysis for visible stems and elements."""

import json
from pathlib import Path


_STEMS = {
    "甲": ("Wood", "Yang"),
    "乙": ("Wood", "Yin"),
    "丙": ("Fire", "Yang"),
    "丁": ("Fire", "Yin"),
    "戊": ("Earth", "Yang"),
    "己": ("Earth", "Yin"),
    "庚": ("Metal", "Yang"),
    "辛": ("Metal", "Yin"),
    "壬": ("Water", "Yang"),
    "癸": ("Water", "Yin"),
}

_BRANCH_ELEMENTS = {
    "子": "Water",
    "丑": "Earth",
    "寅": "Wood",
    "卯": "Wood",
    "辰": "Earth",
    "巳": "Fire",
    "午": "Fire",
    "未": "Earth",
    "申": "Metal",
    "酉": "Metal",
    "戌": "Earth",
    "亥": "Water",
}

_HIDDEN_STEMS = {
    "子": ("癸",),
    "丑": ("己", "癸", "辛"),
    "寅": ("甲", "丙", "戊"),
    "卯": ("乙",),
    "辰": ("戊", "乙", "癸"),
    "巳": ("丙", "戊", "庚"),
    "午": ("丁", "己"),
    "未": ("己", "丁", "乙"),
    "申": ("庚", "壬", "戊"),
    "酉": ("辛",),
    "戌": ("戊", "辛", "丁"),
    "亥": ("壬", "甲"),
}

_ELEMENTS = ("Wood", "Fire", "Earth", "Metal", "Water")
_GENERATES = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood",
}
_CONTROLS = {
    "Wood": "Earth",
    "Earth": "Water",
    "Water": "Fire",
    "Fire": "Metal",
    "Metal": "Wood",
}

_TEN_GODS = {
    ("same", "same"): ("Friend", "比肩"),
    ("same", "opposite"): ("Rob Wealth", "劫財"),
    ("output", "same"): ("Eating God", "食神"),
    ("output", "opposite"): ("Hurting Officer", "傷官"),
    ("wealth", "same"): ("Indirect Wealth", "偏財"),
    ("wealth", "opposite"): ("Direct Wealth", "正財"),
    ("power", "same"): ("Seven Killings", "七殺"),
    ("power", "opposite"): ("Direct Officer", "正官"),
    ("resource", "same"): ("Indirect Resource", "偏印"),
    ("resource", "opposite"): ("Direct Resource", "正印"),
}
_REFERENCE_PATH = Path(__file__).parent / "data" / "reference_bazi.json"
_REFERENCE_CACHE = None


def _ten_god(day_stem, other_stem):
    day_element, day_polarity = _STEMS[day_stem]
    other_element, other_polarity = _STEMS[other_stem]
    polarity = "same" if day_polarity == other_polarity else "opposite"

    if day_element == other_element:
        relationship = "same"
    elif _GENERATES[day_element] == other_element:
        relationship = "output"
    elif _CONTROLS[day_element] == other_element:
        relationship = "wealth"
    elif _CONTROLS[other_element] == day_element:
        relationship = "power"
    else:
        relationship = "resource"

    english, chinese = _TEN_GODS[(relationship, polarity)]
    return f"{english} ({chinese})"


def analyze_bazi(four_pillars_dict):
    """Analyze the Day Master, visible-stem Ten Gods, and visible elements."""
    required = ("year", "month", "day", "hour")
    if not isinstance(four_pillars_dict, dict):
        raise TypeError("four_pillars_dict must be a dictionary.")

    pillars = {}
    for key in required:
        pillar = four_pillars_dict.get(key)
        if not isinstance(pillar, str) or len(pillar) != 2:
            raise ValueError(f"{key!r} must be a two-character stem-branch pillar.")
        stem, branch = pillar
        if stem not in _STEMS:
            raise ValueError(f"Unknown Heavenly Stem {stem!r} in {key!r}.")
        if branch not in _BRANCH_ELEMENTS:
            raise ValueError(f"Unknown Earthly Branch {branch!r} in {key!r}.")
        pillars[key] = (stem, branch)

    day_stem = pillars["day"][0]
    day_element, day_polarity = _STEMS[day_stem]
    ten_gods = {
        f"{key}_stem": _ten_god(day_stem, pillars[key][0])
        for key in ("year", "month", "hour")
    }
    ten_god_names = {
        key: _TEN_GODS_BY_DISPLAY[display]
        for key, display in ten_gods.items()
    }
    hidden_ten_gods = []
    hidden_ten_god_names = []
    for _, branch in pillars.values():
        for hidden_stem in _HIDDEN_STEMS[branch]:
            display = _ten_god(day_stem, hidden_stem)
            name = _TEN_GODS_BY_DISPLAY[display]
            if name not in hidden_ten_god_names:
                hidden_ten_gods.append(display)
                hidden_ten_god_names.append(name)

    elemental_balance = {element: 0 for element in _ELEMENTS}
    for stem, branch in pillars.values():
        elemental_balance[_STEMS[stem][0]] += 1
        elemental_balance[_BRANCH_ELEMENTS[branch]] += 1

    return {
        "day_master": f"{day_polarity} {day_element} ({day_stem})",
        "day_master_stem": day_stem,
        "ten_gods": ten_gods,
        "ten_god_names": ten_god_names,
        "hidden_ten_gods": hidden_ten_gods,
        "hidden_ten_god_names": hidden_ten_god_names,
        "elemental_balance": elemental_balance,
    }


_TEN_GODS_BY_DISPLAY = {
    f"{english} ({chinese})": chinese
    for english, chinese in _TEN_GODS.values()
}


def _load_bazi_reference():
    global _REFERENCE_CACHE
    if _REFERENCE_CACHE is None:
        with _REFERENCE_PATH.open(encoding="utf-8") as reference_file:
            _REFERENCE_CACHE = json.load(reference_file)
    return _REFERENCE_CACHE


def get_bazi_reference(bazi_data):
    """Return labeled modern symbolic reference meanings for a BaZi result."""
    reference = _load_bazi_reference()
    lines = ["BaZi reference (modern symbolic summaries):"]

    day_master_stem = bazi_data["day_master_stem"]
    day_master = next(
        entry for entry in reference["day_masters"]
        if entry["stem"] == day_master_stem
    )
    lines.append(
        f"Day Master — {day_master['display_name']}: {day_master['summary_en']} "
        f"{day_master['disclaimer']}"
    )

    ten_god_by_name = {
        entry["name_zh"]: entry for entry in reference["ten_gods"]
    }
    distinct_gods = dict.fromkeys(bazi_data["ten_god_names"].values())
    for name_zh in distinct_gods:
        ten_god = ten_god_by_name[name_zh]
        lines.append(
            f"Ten God — {ten_god['display_name']}: {ten_god['meaning_en']} "
            f"{ten_god['disclaimer']}"
        )

    hidden_ten_god_names = bazi_data.get("hidden_ten_god_names")
    if hidden_ten_god_names:
        hidden_meanings = []
        for name_zh in dict.fromkeys(hidden_ten_god_names):
            ten_god = ten_god_by_name[name_zh]
            hidden_meanings.append(
                f"{ten_god['display_name']}: {ten_god['meaning_en']} "
                f"{ten_god['disclaimer']}"
            )
        lines.append("Hidden Ten Gods (藏干): " + "; ".join(hidden_meanings))

    for source in reference.get("source_notes", []):
        lines.append(
            f"Historical source locator — {source['title_en']} "
            f"({source['source_type']}; provenance {source['verification_status']}): "
            f"{source['url']}. {source['scope_note']}"
        )

    element_by_state = {
        (entry["element"], entry["state"]): entry
        for entry in reference["elemental_counts"]
    }
    for element, count in bazi_data["elemental_balance"].items():
        state = "Absent" if count == 0 else "High" if count >= 3 else None
        if state is None:
            continue
        entry = element_by_state[(element, state)]
        lines.append(
            f"Visible element count — {element} ({state}, {count}): "
            f"{entry['meaning_en']} {entry['disclaimer']}"
        )

    return "\n".join(lines)
