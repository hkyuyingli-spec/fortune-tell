"""Simplified BaZi analysis for visible stems and elements."""

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

    elemental_balance = {element: 0 for element in _ELEMENTS}
    for stem, branch in pillars.values():
        elemental_balance[_STEMS[stem][0]] += 1
        elemental_balance[_BRANCH_ELEMENTS[branch]] += 1

    return {
        "day_master": f"{day_polarity} {day_element} ({day_stem})",
        "ten_gods": ten_gods,
        "elemental_balance": elemental_balance,
    }
