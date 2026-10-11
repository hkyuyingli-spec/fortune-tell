"""
period_engine.py - time-period layer for the chat (Part 2).

Adds to the natal chart the cycle positions for a chosen period:
  - 10-year cycle (大限): which natal palace the current decade sits in
  - Yearly cycle (流年):  which natal palace the lunar year's branch falls on
  - Monthly cycle (流月): which natal palace the lunar month falls on
                          (method: iztro's, via the birth month and birth hour)

Formulas were cross-checked against iztro on 600 random birth/target dates (0 mismatches).
Not included yet: the Four Transformations and auxiliary stars.

Public functions:
    today_for_tz(tz_name)
    resolve_period(choice, year, month, tz_name)  -> (target_date, scope)
    compute_period(zw, target_date, scope)         -> dict
    format_period_context(info, lang)              -> text for the AI
    period_label(info, lang)                       -> short label for the user
    render_period_selector(st, bc, zw, lang)       -> draws the selector in Streamlit and
                                                      stores the AI text in st.session_state["period_ctx"]
"""
import datetime

import sxtwl

from calendar_engine import DI_ZHI, TIAN_GAN
from glossary import term, translate_pillar
from ziwei_engine import PALACE_NAMES, YIN_INDEX, fix12

# ------------------------------------------------------------------ calendar helpers


def lunar_of(d: datetime.date) -> dict:
    day = sxtwl.fromSolar(d.year, d.month, d.day)
    return {
        "year": day.getLunarYear(),       # changes at lunar new year
        "month": day.getLunarMonth(),
        "day": day.getLunarDay(),
        "leap": bool(day.isLunarLeap()),
    }


def year_gz(lunar_year: int) -> str:
    return TIAN_GAN[(lunar_year - 4) % 10] + DI_ZHI[(lunar_year - 4) % 12]


def today_for_tz(tz_name=None) -> datetime.date:
    """Today's date in the user's timezone (falls back to the server date)."""
    if tz_name:
        try:
            from zoneinfo import ZoneInfo
            return datetime.datetime.now(ZoneInfo(tz_name)).date()
        except Exception:
            pass
    return datetime.date.today()


def resolve_period(choice, year=None, month=None, tz_name=None):
    """choice: 'this_year' | 'this_month' | 'custom'. Returns (target_date, scope)."""
    if choice == "this_year":
        return today_for_tz(tz_name), "year"
    if choice == "this_month":
        return today_for_tz(tz_name), "month"
    year = int(year)
    if month:
        return datetime.date(year, int(month), 15), "month"   # lunar month containing the 15th
    return datetime.date(year, 7, 1), "year"                   # lunar year containing 1 July


def palace_name_at(zw, p: int) -> str:
    """Natal palace name (Chinese) at internal position p (寅 = 0)."""
    return PALACE_NAMES[(zw.soul_p - p) % 12]


# ------------------------------------------------------------------ main calculation


def compute_period(zw, target: datetime.date, scope: str = "year") -> dict:
    bc = zw.chart
    birth = lunar_of(datetime.date(bc.solar_year, bc.solar_month, bc.solar_day))
    tgt = lunar_of(target)

    age = tgt["year"] - birth["year"] + 1          # Chinese (nominal) age, lunar-year based
    year_branch_idx = (tgt["year"] - 4) % 12        # 子 = 0
    year_p = fix12(year_branch_idx - YIN_INDEX)     # palace position of the year branch (寅 = 0)

    decade = None
    for p, d in zw.decades_by_p.items():
        lo, hi = d["range"]
        if lo <= age <= hi:
            decade = {"range": (lo, hi), "palace": palace_name_at(zw, p)}
            break

    leap_add = 1 if (birth["leap"] and birth["day"] > 15) else 0
    date_leap_add = 1 if (tgt["leap"] and tgt["day"] > 15) else 0
    hour_idx = DI_ZHI.index(bc.hour_gz[1])
    month_p = fix12(year_p - (birth["month"] + leap_add) + hour_idx + (tgt["month"] + date_leap_add))

    return {
        "target": target,
        "scope": scope,
        "lunar": tgt,
        "year_gz": year_gz(tgt["year"]),
        "age": age,
        "first_decade_age": min(d["range"][0] for d in zw.decades_by_p.values()),
        "decade": decade,
        "year_palace": palace_name_at(zw, year_p),
        "month_palace": palace_name_at(zw, month_p),
    }


# ------------------------------------------------------------------ text for the AI and the user

_MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "id": ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
           "Agustus", "September", "Oktober", "November", "Desember"],
}

_T = {
    "en": {
        "ref": "Reference date: {date} (lunar year {gz}, lunar month {m}{leap})",
        "age": "Age on that date (Chinese count): {age}",
        "decade": "10-year cycle: ages {lo}-{hi}, located in the {palace} palace",
        "decade_none": "10-year cycle: has not started yet (it begins at age {n})",
        "year": "Yearly cycle ({gz}): located in the {palace} palace",
        "month": "Monthly cycle (lunar month {m}): located in the {palace} palace",
        "note": "Only the cycle positions above are calculated. The Four Transformations and auxiliary stars are not calculated, so make no claims about them.",
        "leap": ", leap month",
        "label_year": "Year {y} (lunar year {gz})",
        "label_month": "{mon} {y} (lunar year {gz}, lunar month {m})",
    },
    "id": {
        "ref": "Tanggal acuan: {date} (tahun lunar {gz}, bulan lunar {m}{leap})",
        "age": "Usia pada tanggal itu (hitungan Tiongkok): {age}",
        "decade": "Siklus 10 tahun: usia {lo}-{hi}, berada di istana {palace}",
        "decade_none": "Siklus 10 tahun: belum dimulai (mulai pada usia {n})",
        "year": "Siklus tahunan ({gz}): berada di istana {palace}",
        "month": "Siklus bulanan (bulan lunar {m}): berada di istana {palace}",
        "note": "Hanya posisi siklus di atas yang dihitung. Empat Transformasi dan bintang tambahan belum dihitung, jadi jangan membuat klaim tentang itu.",
        "leap": ", bulan kabisat",
        "label_year": "Tahun {y} (tahun lunar {gz})",
        "label_month": "{mon} {y} (tahun lunar {gz}, bulan lunar {m})",
    },
    "zh": {
        "ref": "運限參考日期：{date}（農曆{gz}年{m}月{leap}）",
        "age": "該日期的虛歲：{age}",
        "decade": "大限：{lo}-{hi}歲，落在{palace}宮",
        "decade_none": "大限：尚未起運（{n}歲起運）",
        "year": "流年（{gz}）：落在{palace}宮",
        "month": "流月（農曆{m}月）：落在{palace}宮",
        "note": "目前只計算了上述運限宮位，尚未計算四化與輔星，請勿對這些內容作任何斷言。",
        "leap": "（閏月）",
        "label_year": "{y}年（農曆{gz}年）",
        "label_month": "{y}年{mon}月（農曆{gz}年{m}月）",
    },
}


def _lang(lang):
    return lang if lang in _T else "en"


def _gz(gz, lang):
    return gz if lang == "zh" else translate_pillar(gz, lang)


def _palace(zh, lang):
    return term(zh, lang).replace("宮", "") if lang == "zh" else term(zh, lang)


def format_period_context(info: dict, lang: str) -> str:
    lang = _lang(lang)
    T = _T[lang]
    lun = info["lunar"]
    gz = _gz(info["year_gz"], lang)
    lines = [
        T["ref"].format(date=info["target"].isoformat(), gz=gz, m=lun["month"],
                        leap=T["leap"] if lun["leap"] else ""),
        T["age"].format(age=info["age"]),
    ]
    if info["decade"]:
        d = info["decade"]
        lines.append(T["decade"].format(lo=d["range"][0], hi=d["range"][1],
                                        palace=_palace(d["palace"], lang)))
    else:
        lines.append(T["decade_none"].format(n=info["first_decade_age"]))
    lines.append(T["year"].format(gz=gz, palace=_palace(info["year_palace"], lang)))
    if info["scope"] == "month":
        lines.append(T["month"].format(m=lun["month"], palace=_palace(info["month_palace"], lang)))
    lines.append(T["note"])
    return "\n".join(lines)


def period_label(info: dict, lang: str) -> str:
    lang = _lang(lang)
    T = _T[lang]
    lun = info["lunar"]
    gz = _gz(info["year_gz"], lang)
    t = info["target"]
    if info["scope"] == "month":
        mon = str(t.month) if lang == "zh" else _MONTHS[lang][t.month - 1]
        return T["label_month"].format(mon=mon, y=t.year, gz=gz, m=lun["month"])
    return T["label_year"].format(y=lun["year"], gz=gz)


# ------------------------------------------------------------------ Streamlit selector

PERIOD_UI = {
    "en": {"header": "Which period would you like to know about?",
           "this_year": "This year", "this_month": "This month", "custom": "Choose year / month",
           "year": "Year", "month": "Month (optional)", "whole_year": "Whole year",
           "reading_for": "Reading for: {label}"},
    "id": {"header": "Periode mana yang ingin Anda ketahui?",
           "this_year": "Tahun ini", "this_month": "Bulan ini", "custom": "Pilih tahun / bulan",
           "year": "Tahun", "month": "Bulan (opsional)", "whole_year": "Satu tahun penuh",
           "reading_for": "Pembacaan untuk: {label}"},
    "zh": {"header": "你想了解哪個時間段？",
           "this_year": "今年", "this_month": "本月", "custom": "選擇年份／月份",
           "year": "年份", "month": "月份（可不選）", "whole_year": "整年",
           "reading_for": "解讀時間：{label}"},
}


def render_period_selector(st, bc, zw, lang):
    ui = PERIOD_UI[_lang(lang)]
    tz = None
    try:
        tz = st.context.timezone          # the user's browser timezone
    except Exception:
        pass

    choice = st.radio(
        ui["header"], ["this_year", "this_month", "custom"],
        format_func=lambda k: ui[k], index=0, horizontal=True, key="period_choice",
    )
    year = month = None
    if choice == "custom":
        this_year = today_for_tz(tz).year
        years = [y for y in range(this_year - 10, this_year + 6) if y >= bc.solar_year] or [this_year]
        default_idx = years.index(this_year) if this_year in years else 0
        c1, c2 = st.columns(2)
        with c1:
            year = st.selectbox(ui["year"], years, index=default_idx, key="period_year")
        with c2:
            month = st.selectbox(
                ui["month"], [0] + list(range(1, 13)),
                format_func=lambda m: ui["whole_year"] if m == 0 else str(m), key="period_month",
            ) or None

    target, scope = resolve_period(choice, year, month, tz)
    info = compute_period(zw, target, scope)
    st.session_state["period_ctx"] = format_period_context(info, lang)
    st.caption(ui["reading_for"].format(label=period_label(info, lang)))
    return info
