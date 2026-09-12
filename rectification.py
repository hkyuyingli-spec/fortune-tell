"""
定盤 (birth-time rectification).

When the user doesn't know their exact birth time, Zi Wei Dou Shu's life
palace / body palace / star placement is genuinely undetermined -- not
"less precise", literally a different chart for each of the 12 two-hour
blocks (see the sensitivity analysis this module's design is based on).

Standard professional practice ("定盤") is to generate every possible
chart for the birth date and narrow them down using known facts about the
person's actual life -- personality, major life turning points, etc. This
module automates a simplified version of that process:

  1. generate_candidates()  -- all 12 two-hour-block charts for a date+gender
  2. personality_question() -- ask which life-palace description resonates
  3. narrow_by_turning_point() -- ask roughly when a major life turning point happened
  4. narrow_by_personality() -- filter candidates by the personality answer

This is a simplified, semi-automated version of a skilled manual process.
It narrows the field; it does not guarantee a unique, provably-correct
answer -- classical practice acknowledges some birth times (especially
right at the 子時/子時 boundary) are genuinely hard to pin down even by
an experienced practitioner.
"""
from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart
from interpretation import MAJOR_STAR_BLURB

SHICHEN_LABELS = [
    ("早子時", "00:00–00:59"), ("丑時", "01:00–02:59"), ("寅時", "03:00–04:59"),
    ("卯時", "05:00–06:59"), ("辰時", "07:00–08:59"), ("巳時", "09:00–10:59"),
    ("午時", "11:00–12:59"), ("未時", "13:00–14:59"), ("申時", "15:00–16:59"),
    ("酉時", "17:00–18:59"), ("戌時", "19:00–20:59"), ("亥時", "21:00–22:59"),
    ("夜子時", "23:00–23:59"),
]

# Representative clock hour for each of the 13 slots (index 12 = late-zi,
# handled specially by BirthChart's is_late_zi day-rollover logic).
_REPRESENTATIVE_HOUR = {0: 0, 12: 23}


class Candidate:
    def __init__(self, shichen_idx, year, month, day, gender):
        self.shichen_idx = shichen_idx
        self.label, self.time_range = SHICHEN_LABELS[shichen_idx]
        hour = _REPRESENTATIVE_HOUR.get(shichen_idx, shichen_idx * 2)
        self.bc = BirthChart(year, month, day, hour, 0)
        self.zw = ZiWeiChart(self.bc, gender)
        life_row = self.zw.palace_table()[0]
        self.life_stars = life_row["stars"]
        self.life_stem_branch = life_row["stem"] + life_row["branch"]
        self.bureau_number = self.zw.bureau_number
        self.decade_start = self.zw.decades_by_p[self.zw.soul_p]["range"][0]

    def personality_text(self, lang="zh"):
        default_texts = {
            "zh": "個性較不明顯外顯，容易受環境與身邊的人影響，可塑性高。",
            "en": "A less outwardly obvious personality — easily shaped by environment and the people around you, highly adaptable.",
            "id": "Kepribadian kurang tampak keluar — mudah dipengaruhi lingkungan dan orang sekitar, sangat mudah beradaptasi.",
        }
        if not self.life_stars:
            return default_texts[lang]
        return " ".join(MAJOR_STAR_BLURB.get(s, {}).get(lang, "") for s in self.life_stars)

    def decade_boundaries(self):
        """Ages at which this candidate's decade cycle rolls over (useful
        for asking 'when did something big change')."""
        return [self.decade_start + 10 * i for i in range(12)]


def generate_candidates(year, month, day, gender):
    return [Candidate(i, year, month, day, gender) for i in range(13)]


def personality_question(candidates, lang="zh"):
    """Group candidates by DISTINCT personality text, so the user picks
    from real, non-duplicate options rather than 12 near-identical ones."""
    groups = {}
    for c in candidates:
        key = c.personality_text(lang)
        groups.setdefault(key, []).append(c)
    # Return as list of (text, [shichen_idx,...]) sorted for stable display
    return [(text, [c.shichen_idx for c in group]) for text, group in groups.items()]


def narrow_by_personality(candidates, chosen_shichen_indices):
    return [c for c in candidates if c.shichen_idx in chosen_shichen_indices]


def narrow_by_turning_point(candidates, approx_age, tolerance=3):
    """Keep candidates whose decade cycle rolls over within `tolerance`
    years of the age the user reports as a major turning point.

    Returns (result_candidates, did_narrow: bool) -- the caller needs to
    know WHY the list didn't shrink: "this question wasn't useful for this
    birth date" is a different situation from "you narrowed it to one",
    and silently returning the same list for both looked identical to the
    user before this fix."""
    kept = []
    for c in candidates:
        boundaries = c.decade_boundaries()
        if any(abs(approx_age - b) <= tolerance for b in boundaries):
            kept.append(c)
    if kept:
        return kept, True
    return candidates, False
