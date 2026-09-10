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
    ("子時", "23:00–00:59"), ("丑時", "01:00–02:59"), ("寅時", "03:00–04:59"),
    ("卯時", "05:00–06:59"), ("辰時", "07:00–08:59"), ("巳時", "09:00–10:59"),
    ("午時", "11:00–12:59"), ("未時", "13:00–14:59"), ("申時", "15:00–16:59"),
    ("酉時", "17:00–18:59"), ("戌時", "19:00–20:59"), ("亥時", "21:00–22:59"),
]


class Candidate:
    def __init__(self, shichen_idx, year, month, day, gender):
        self.shichen_idx = shichen_idx
        self.label, self.time_range = SHICHEN_LABELS[shichen_idx]
        hour = shichen_idx * 2  # representative hour within the block
        self.bc = BirthChart(year, month, day, hour, 0)
        self.zw = ZiWeiChart(self.bc, gender)
        life_row = self.zw.palace_table()[0]
        self.life_stars = life_row["stars"]
        self.life_stem_branch = life_row["stem"] + life_row["branch"]
        self.bureau_number = self.zw.bureau_number
        self.decade_start = self.zw.decades_by_p[self.zw.soul_p]["range"][0]

    def personality_text(self):
        if not self.life_stars:
            return "個性較不明顯外顯，容易受環境與身邊的人影響，可塑性高。"
        return " ".join(MAJOR_STAR_BLURB.get(s, "") for s in self.life_stars)

    def decade_boundaries(self):
        """Ages at which this candidate's decade cycle rolls over (useful
        for asking 'when did something big change')."""
        return [self.decade_start + 10 * i for i in range(12)]


def generate_candidates(year, month, day, gender):
    return [Candidate(i, year, month, day, gender) for i in range(12)]


def personality_question(candidates):
    """Group candidates by DISTINCT personality text, so the user picks
    from real, non-duplicate options rather than 12 near-identical ones."""
    groups = {}
    for c in candidates:
        key = c.personality_text()
        groups.setdefault(key, []).append(c)
    # Return as list of (text, [shichen_idx,...]) sorted for stable display
    return [(text, [c.shichen_idx for c in group]) for text, group in groups.items()]


def narrow_by_personality(candidates, chosen_shichen_indices):
    return [c for c in candidates if c.shichen_idx in chosen_shichen_indices]


def narrow_by_turning_point(candidates, approx_age, tolerance=3):
    """Keep candidates whose decade cycle rolls over within `tolerance`
    years of the age the user reports as a major turning point. Never
    narrows to zero -- if nothing matches within tolerance, the question
    wasn't useful for this birth date, so we leave the set untouched."""
    kept = []
    for c in candidates:
        boundaries = c.decade_boundaries()
        if any(abs(approx_age - b) <= tolerance for b in boundaries):
            kept.append(c)
    return kept or candidates
