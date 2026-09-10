"""
Zi Wei Dou Shu (紫微斗數) core chart engine.

The placement formulas here are ported and validated against the algorithm
used by `iztro` (SylarLong/iztro), an open-source (MIT licensed), widely used
Zi Wei Dou Shu library -- cross-checked against its published source and
against generated reference charts for multiple test birthdates before
being trusted here.

Scope of this module (explicitly, so it's clear what's *not* included yet):
  INCLUDED : life palace (命宮), body palace (身宮), five-element bureau
             (五行局), the 12 palaces with correct stem+branch, all 14
             major stars (十四主星), and the decade luck cycle (大限)
             sequence with age ranges.
  NOT YET  : the ~100 auxiliary/minor stars, the Four Transformations
             (四化) flying-palace analysis, and full annual/monthly/daily
             drill-down (流年/流月/流日 star overlays). Those are a
             separate, much larger phase.
"""
from calendar_engine import TIAN_GAN, DI_ZHI, BirthChart

PALACE_NAMES = [
    "命宮", "兄弟", "夫妻", "子女", "財帛", "疾厄",
    "遷移", "交友", "官祿", "田宅", "福德", "父母",
]

# 五虎遁: year stem -> stem at the 寅 palace
TIGER_RULE = {
    "甲": "丙", "己": "丙",
    "乙": "戊", "庚": "戊",
    "丙": "庚", "辛": "庚",
    "丁": "壬", "壬": "壬",
    "戊": "甲", "癸": "甲",
}

FIVE_ELEMENTS_TABLE = {1: ("木", 3), 2: ("金", 4), 3: ("水", 2), 4: ("火", 6), 5: ("土", 5)}

# offsets (寅=0 internal index), counterclockwise from Zi Wei
ZIWEI_GROUP = ["紫微", "天機", "", "太陽", "武曲", "天同", "", "", "廉貞"]
# offsets (寅=0 internal index), clockwise from Tian Fu
TIANFU_GROUP = ["天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "", "", "", "破軍"]

# 命主 (Life Star) lookup — keyed by the Life Palace's earthly branch
# 身主 (Body Star) lookup — keyed by the YEAR's earthly branch (not the body palace)
# Both ported from iztro's earthlyBranches data table.
MING_ZHU_TABLE = {
    "子": "貪狼", "丑": "巨門", "寅": "祿存", "卯": "文曲",
    "辰": "廉貞", "巳": "武曲", "午": "破軍", "未": "武曲",
    "申": "廉貞", "酉": "文曲", "戌": "祿存", "亥": "巨門",
}
SHEN_ZHU_TABLE = {
    "子": "火星", "丑": "天相", "寅": "天梁", "卯": "天同",
    "辰": "文昌", "巳": "天機", "午": "火星", "未": "天相",
    "申": "天梁", "酉": "天同", "戌": "文昌", "亥": "天機",
}

YIN_INDEX = DI_ZHI.index("寅")  # standard-branch index of 寅 = 2


def fix12(x: int) -> int:
    return x % 12


def fix10(x: int) -> int:
    return x % 10


class ZiWeiChart:
    def __init__(self, chart: BirthChart, gender: str):
        assert gender in ("male", "female")
        self.chart = chart
        self.gender = gender

        self._compute_soul_and_body()
        self._compute_five_elements_bureau()
        self._compute_palace_stems_and_branches()
        self._compute_ziwei_tianfu_index()
        self._compute_major_stars()
        self._compute_decades()
        self._compute_ming_zhu_shen_zhu()

    # ---- 1. Life palace (命宮) & Body palace (身宮) ----
    def _compute_soul_and_body(self):
        month = self.chart.zi_wei_month_number()
        hour_branch_std_idx = DI_ZHI.index(self.chart.hour_gz[1])
        # p-index space: 寅 = 0
        self.soul_p = fix12((month - 1) - hour_branch_std_idx)
        self.body_p = fix12((month - 1) + hour_branch_std_idx)

        self.soul_std = fix12(self.soul_p + YIN_INDEX)  # standard branch index (0=子)
        self.body_std = fix12(self.body_p + YIN_INDEX)

    # ---- 2. Palace heavenly stems (宮干), derived from year stem via 五虎遁 ----
    def _compute_palace_stems_and_branches(self):
        year_stem = self.chart.zi_wei_year_gz[0]
        yin_stem = TIGER_RULE[year_stem]
        yin_stem_idx = TIAN_GAN.index(yin_stem)

        # p index 0..11 -> standard branch idx = p+YIN_INDEX (mod12)
        # stem index = yin_stem_idx + p (mod 10)
        self.palace_branch_std = [fix12(p + YIN_INDEX) for p in range(12)]
        self.palace_stem_idx = [fix10(yin_stem_idx + p) for p in range(12)]

        self.soul_stem = TIAN_GAN[self.palace_stem_idx[self.soul_p]]
        self.soul_branch = DI_ZHI[self.soul_std]

    # ---- 3. Five Elements Bureau (五行局), from life palace stem+branch ----
    def _compute_five_elements_bureau(self):
        # needs soul stem/branch, so make sure soul is computed first (it is, via _compute_soul_and_body)
        pass  # computed lazily below once palace stems are known

    def _finish_bureau(self):
        stem_idx = TIAN_GAN.index(self.soul_stem)
        branch_idx = DI_ZHI.index(self.soul_branch)
        stem_num = stem_idx // 2 + 1
        branch_num = (branch_idx % 6) // 2 + 1
        idx = stem_num + branch_num
        while idx > 5:
            idx -= 5
        element, bureau_num = FIVE_ELEMENTS_TABLE[idx]
        self.bureau_element = element
        self.bureau_number = bureau_num
        self.bureau_name = f"{element}{['','一','二','三','四','五','六'][bureau_num]}局"

    # ---- 4. Zi Wei / Tian Fu star index ----
    def _compute_ziwei_tianfu_index(self):
        self._finish_bureau()
        day = self.chart.ziwei_lunar_day
        B = self.bureau_number

        offset = -1
        remainder = -1
        quotient = 0
        while remainder != 0:
            offset += 1
            divisor = day + offset
            quotient = divisor // B
            remainder = divisor % B
        quotient = quotient % 12
        ziwei_p = quotient - 1
        if offset % 2 == 0:
            ziwei_p += offset
        else:
            ziwei_p -= offset
        self.ziwei_p = fix12(ziwei_p)
        self.tianfu_p = fix12(12 - self.ziwei_p)

    # ---- 5. Place the 14 major stars into the 12 palaces (p-index space) ----
    def _compute_major_stars(self):
        self.stars_by_p = {p: [] for p in range(12)}
        for i, name in enumerate(ZIWEI_GROUP):
            if name:
                self.stars_by_p[fix12(self.ziwei_p - i)].append(name)
        for i, name in enumerate(TIANFU_GROUP):
            if name:
                self.stars_by_p[fix12(self.tianfu_p + i)].append(name)

    # ---- 6. Decade luck cycles (大限) ----
    def _compute_decades(self):
        year_branch_idx = DI_ZHI.index(self.chart.zi_wei_year_gz[1])
        year_is_yang = (year_branch_idx % 2 == 0)
        forward = (year_is_yang and self.gender == "male") or ((not year_is_yang) and self.gender == "female")

        year_stem = self.chart.zi_wei_year_gz[0]
        yin_stem_idx = TIAN_GAN.index(TIGER_RULE[year_stem])

        self.decades_by_p = {}
        for i in range(12):
            p = fix12(self.soul_p + i) if forward else fix12(self.soul_p - i)
            start_age = self.bureau_number + 10 * i
            stem_idx = fix10(yin_stem_idx + p)
            self.decades_by_p[p] = {
                "range": (start_age, start_age + 9),
                "stem": TIAN_GAN[stem_idx],
                "branch": DI_ZHI[fix12(p + YIN_INDEX)],
            }
        self.decade_direction = "forward" if forward else "backward"

    # ---- 7. 命主 / 身主 (Life Star / Body Star) ----
    def _compute_ming_zhu_shen_zhu(self):
        year_branch = self.chart.zi_wei_year_gz[1]
        self.ming_zhu = MING_ZHU_TABLE[self.soul_branch]   # keyed by Life Palace branch
        self.shen_zhu = SHEN_ZHU_TABLE[year_branch]         # keyed by year branch

    # ---- Public: full palace table, in fixed life-palace-first order ----
    def palace_table(self):
        """Returns the 12 palaces starting at the Life Palace, going the
        traditional counter-clockwise direction (命,兄弟,夫妻,...)."""
        rows = []
        for i, pname in enumerate(PALACE_NAMES):
            p = fix12(self.soul_p - i)
            rows.append({
                "palace": pname,
                "stem": TIAN_GAN[self.palace_stem_idx[p]],
                "branch": DI_ZHI[fix12(p + YIN_INDEX)],
                "stars": self.stars_by_p[p],
                "is_body_palace": (p == self.body_p),
                "decade": self.decades_by_p[p],
            })
        return rows

    def current_year_palace(self, year: int):
        """Which palace does a given (Gregorian, for simplicity) year's
        branch fall on -- a simple 流年 pointer, not a full annual overlay."""
        # Chinese year branch cycles with a known anchor: 1984 = 甲子 (branch 子, idx0)
        branch_idx = (year - 1984) % 12
        target_std = branch_idx
        for i, pname in enumerate(PALACE_NAMES):
            p = fix12(self.soul_p - i)
            if fix12(p + YIN_INDEX) == target_std:
                return pname
        return None
