"""
Shared lunar-calendar engine.

Backed by `sxtwl` (a Python binding of 寿星天文历, an astronomically-computed
Chinese calendar library), so month-pillar and solar-term boundaries are
computed correctly rather than approximated.

This module is the single source of truth for:
  - Gregorian <-> lunar date conversion
  - BaZi (Four Pillars / 八字): year, month, day, hour ganzhi
  - Julian-day-based utilities used by the Zi Wei engine

BaZi note: the month pillar here follows the traditional 节气 (solar term)
convention, which is the professionally correct method for Four Pillars.
Zi Wei Dou Shu uses a different convention (calendar lunar month) for its
own palace placement -- see ziwei_engine.py.
"""
import sxtwl
import datetime

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# Standard 12 two-hour blocks. index 0 = 23:00-00:59 (子时) ... index 11 = 21:00-22:59 (亥时)
def hour_to_shichen_index(hour: int) -> int:
    """Map a 24h clock hour (0-23) to the standard 12 branch-hour index (0=子...11=亥)."""
    h = hour % 24
    return ((h + 1) // 2) % 12


class FourPillars:
    def __init__(self, year_gz, month_gz, day_gz, hour_gz):
        self.year = year_gz
        self.month = month_gz
        self.day = day_gz
        self.hour = hour_gz

    def as_dict(self):
        return {
            "year": self.year, "month": self.month,
            "day": self.day, "hour": self.hour,
        }


def _gz(tg_idx, dz_idx):
    return TIAN_GAN[tg_idx] + DI_ZHI[dz_idx]


# 五虎遁 (year stem -> stem at the 寅 month/palace). Duplicated locally (also
# used by ziwei_engine.py) to avoid a circular import.
TIGER_RULE_LOCAL = {
    "甲": "丙", "己": "丙",
    "乙": "戊", "庚": "戊",
    "丙": "庚", "辛": "庚",
    "丁": "壬", "壬": "壬",
    "戊": "甲", "癸": "甲",
}

JIE_TO_MONTH_PERIOD = {3: 1, 5: 2, 7: 3, 9: 4, 11: 5, 13: 6, 15: 7, 17: 8, 19: 9, 21: 10, 23: 11, 1: 12}


def _jieqi_moment(year, jq_index):
    for j in sxtwl.getJieQiByYear(year):
        if j.jqIndex == jq_index:
            dd = sxtwl.JD2DD(j.jd)
            return (int(dd.Y), int(dd.M), int(dd.D), dd.h * 60 + dd.m)
    return None


class BirthChart:
    """Computes and holds every raw calendar fact needed by both the BaZi
    and Zi Wei engines, for one birth moment.

    `sxtwl`'s built-in getYearGZ()/getMonthGZ() switch pillars at *day*
    granularity on solar-term boundary days, not at the exact hour/minute
    of the term. That's wrong for anyone born on one of the ~13 days a
    year where a solar term actually lands (立春 for the year pillar,
    the 12 月节 for the month pillar) -- so we re-derive both precisely
    against the exact solar-term moment.
    """

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int = 0):
        self.solar_year, self.solar_month, self.solar_day = year, month, day
        self.hour, self.minute = hour, minute
        self.day_obj = sxtwl.fromSolar(year, month, day)

        self.lunar_year = self.day_obj.getLunarYear()
        self.lunar_month = self.day_obj.getLunarMonth()
        self.lunar_day = self.day_obj.getLunarDay()
        self.is_leap_month = self.day_obj.isLunarLeap()

        self.shichen_index = hour_to_shichen_index(hour)

        # 晚子時 (late zi, 23:00-23:59) vs 早子時 (early zi, 00:00-00:59):
        # both share the same 子 branch, so BaZi's day pillar and the Zi
        # Wei life-palace branch are unaffected. But iztro's default
        # convention (dayDivide='forward', matching common practice) shifts
        # the lunar DAY COUNT used specifically in the 紫微/天府 star
        # placement formula forward by one for late-zi births -- verified
        # against iztro directly: same date, same bureau, genuinely
        # different major-star placement between the two. Confirmed sxtwl's
        # own day pillar does NOT shift at hour 23 (checked directly), so
        # only this one downstream value needs the adjustment.
        self.is_late_zi = (hour % 24) == 23
        if self.is_late_zi:
            # Use the actual next calendar day's lunar day, not raw +1
            # arithmetic -- if birth falls on the last day of a lunar
            # month (e.g. day 30), +1 gives an impossible "day 31" instead
            # of correctly rolling over to day 1 of the next lunar month.
            next_solar = datetime.date(year, month, day) + datetime.timedelta(days=1)
            next_day_obj = sxtwl.fromSolar(next_solar.year, next_solar.month, next_solar.day)
            self.ziwei_lunar_day = next_day_obj.getLunarDay()
        else:
            self.ziwei_lunar_day = self.lunar_day

        dgz = self.day_obj.getDayGZ()
        hgz = self.day_obj.getHourGZ(hour % 24)
        self.day_gz = _gz(dgz.tg, dgz.dz)
        self.hour_gz = _gz(hgz.tg, hgz.dz)

        birth_moment = (year, month, day, hour * 60 + minute)

        # --- precise year pillar (立春-exact) ---
        ygz = self.day_obj.getYearGZ()
        y_tg, y_dz = ygz.tg, ygz.dz
        lichun = _jieqi_moment(year, 3)
        if lichun and (month, day) == (lichun[1], lichun[2]) and birth_moment[3] < lichun[3]:
            y_tg, y_dz = (y_tg - 1) % 10, (y_dz - 1) % 12
        self.year_gz = _gz(y_tg, y_dz)
        self.year_gan_idx, self.year_zhi_idx = y_tg, y_dz

        # --- precise month pillar (月节-exact), derived from the corrected year stem ---
        jie_events = []
        for yy in (year - 1, year, year + 1):
            for j in sxtwl.getJieQiByYear(yy):
                if j.jqIndex in JIE_TO_MONTH_PERIOD:
                    dd = sxtwl.JD2DD(j.jd)
                    moment = (int(dd.Y), int(dd.M), int(dd.D), dd.h * 60 + dd.m)
                    jie_events.append((moment, JIE_TO_MONTH_PERIOD[j.jqIndex]))
        jie_events.sort(key=lambda t: t[0])
        period = None
        for moment, per in jie_events:
            if moment <= birth_moment:
                period = per
            else:
                break
        if period is None:
            period = 12  # birth before the first 立春 in our 3-year window (shouldn't happen in practice)

        yin_stem_idx = TIAN_GAN.index(TIGER_RULE_LOCAL[TIAN_GAN[y_tg]])
        m_tg = (yin_stem_idx + (period - 1)) % 10
        m_dz = (DI_ZHI.index("寅") + (period - 1)) % 12
        self.month_gz = _gz(m_tg, m_dz)

        self.four_pillars = FourPillars(self.year_gz, self.month_gz, self.day_gz, self.hour_gz)

        # --- Zi Wei Dou Shu's OWN year convention: the plain lunar calendar
        # year (switches at Chinese New Year), NOT at 立春. This is a real,
        # separate convention from BaZi's year pillar above -- confirmed
        # against iztro's default 'normal' yearDivide config, which every
        # one of its Zi Wei calculations (palace stems, major stars, decade
        # cycles, minor stars) is built on. Mixing this up is a subtle bug:
        # it only shows up for people born between 立春 and the following
        # Chinese New Year (roughly a 2-3 week window each year).
        zw_stem_idx = (self.lunar_year - 4) % 10
        zw_branch_idx = (self.lunar_year - 4) % 12
        self.zi_wei_year_gz = _gz(zw_stem_idx, zw_branch_idx)

    def zi_wei_month_number(self) -> int:
        """Lunar month number used by Zi Wei Dou Shu palace placement
        (1-12; leap months resolved by the classic 15-day split rule:
        first half of a leap month counts as the base month, second half
        counts as the following month)."""
        m = self.lunar_month
        if self.is_leap_month:
            if self.lunar_day > 15:
                m = m + 1 if m < 12 else 1
        return m
