# 命盤 · Destiny Chart

A Zi Wei Dou Shu (紫微斗數) + BaZi (八字) chart generator, in the spirit of
Click108's free-chart → gated-report structure.

## What this computes (and how it's validated)

- **Calendar engine** (`calendar_engine.py`): Gregorian ↔ lunar conversion
  and the Four Pillars (八字), backed by [`sxtwl`](https://pypi.org/project/sxtwl/)
  (寿星天文历), an astronomically-computed Chinese calendar library.
  Year and month pillars are re-derived against the *exact* solar-term
  moment (立春 for the year, the 12 月節 for the month) rather than
  `sxtwl`'s day-level default, which is wrong for anyone born on the exact
  day a solar term lands.

  Zi Wei Dou Shu uses a **different year and month convention than BaZi**:
  it switches at Chinese New Year (lunar calendar year) and uses the plain
  lunar month, not solar terms. This module exposes both conventions
  separately (`year_gz`/`month_gz` for BaZi, `zi_wei_year_gz`/
  `zi_wei_month_number()` for Zi Wei) so the two systems never get
  cross-contaminated.

- **Zi Wei Dou Shu engine** (`ziwei_engine.py`): life palace (命宮), body
  palace (身宮), life star / body star (命主 / 身主), five-element bureau
  (五行局), all 12 palaces with correct stem+branch, all 14 major stars
  (十四主星), and the decade luck cycle (大限) with age ranges.

  The placement formulas are ported from and cross-validated against
  [`iztro`](https://github.com/SylarLong/iztro) (MIT licensed, ~2k★,
  actively maintained) — a well-established open-source Zi Wei Dou Shu
  library.

- **Birth-time rectification** (`rectification.py`): when the user doesn't
  know their exact birth time, this generates all 12 candidate charts
  (one per two-hour block) and narrows them via a guided Q&A — a
  simplified, semi-automated version of the traditional 定盤 process. It
  narrows the field; it does not claim to find a single provably-correct
  answer.

## Handling unknown birth time (定盤)

Birth time isn't a refinement in this system — it's one of the two direct
inputs to the life-palace formula. Without it, the chart is genuinely
undetermined: the same person's date of birth can produce 12 substantially
different charts (different bureau, different life-palace stars,
different decade cycle) depending on which two-hour block they were born
in. This isn't a corner case; it's the reason professional practice has a
name for dealing with it (定盤 / birth-time rectification): generate every
possible chart and narrow down using known facts about the person's
actual life.

`app.py` now offers two flows:
- **Known time** — the original direct-input flow.
- **Unknown time** — generates all 12 candidates, asks which life-palace
  personality description resonates most, optionally asks roughly when a
  major life turning point happened (matched against each candidate's
  decade-cycle boundaries), and narrows the field. If more than one
  candidate survives, the user picks from a short, real list instead of
  guessing among 12.

This is a genuine simplification of a skilled manual process, not a
replacement for it — flagged as such in the app itself.


Validated against `iztro`'s own output at three levels:

1. `validate.py` — 3 hand-picked cases, manually diffed field-by-field.
2. `accuracy_sweep.py` — 300 randomized birthdates (1950-2025, both
   genders, all 12 two-hour blocks), diffed programmatically across
   bureau, life/body palace, life/body star, and all 12 palaces'
   stem+branch, star placement, and decade range. **300/300 passed.**
3. A targeted edge-case sweep: 5 real leap-lunar-month birthdates + 4
   birthdates landing exactly on a 立春 (solar-term) boundary day,
   including two that fall in the ~2-3 week window between 立春 and the
   following Chinese New Year — the specific window that exposed a real
   bug during development (see below). **9/9 passed.**

**Bugs found and fixed during this validation process** (documented here
rather than swept under the rug):

- `sxtwl`'s year/month pillar switches at *day* granularity on the
  solar-term day itself, not at the exact hour/minute — wrong for anyone
  born on that specific day. Fixed by re-deriving both against the exact
  solar-term timestamp.
- Zi Wei Dou Shu's palace-stem, bureau, and decade-cycle calculations all
  depend on the *lunar calendar year* (switches at Chinese New Year), not
  the 立春-based year used for BaZi. Using the wrong one silently produces
  a fully plausible-looking but wrong chart for anyone born between 立春
  and the following Chinese New Year — roughly a 2-3 week window every
  year. This was caught by the targeted edge-case sweep, not the random
  one, which is why both exist.


- **Interpretation layer** (`interpretation.py`): templated text keyed off
  the real computed chart data (day master, life-palace stars, bureau,
  per-palace stars) — not a random or purely cosmetic layer.

## What's explicitly NOT included yet (next phase)

- The ~100 auxiliary/minor stars (輔星、煞星、桃花星等)
- The Four Transformations (四化) flying-palace analysis
- Full annual/monthly/daily overlay (流年/流月/流日 star recalculation) —
  the current-year palace pointer is a simple branch lookup, not a full
  annual chart
- Leap-month handling uses the common 15-day-split simplification, not a
  full alternate-school treatment

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
calendar_engine.py   — lunar calendar + BaZi four pillars
ziwei_engine.py       — Zi Wei Dou Shu chart engine
interpretation.py     — free-tier / paid-tier text templates
app.py                — Streamlit UI (free chart + gated full report)
validate.py           — cross-check against iztro reference output
```

## Disclaimer

This tool computes a structurally correct traditional chart. It does not
predict the future. Treat the interpretation text as a reflective prompt,
not a factual claim about your life.
