"""
time_engine.py - birth-time handling for the chart (time zone, daylight saving, hour boundaries).

Convention used (the common one in Zi Wei practice and in iztro-based tools):
  * The chart uses the birth place's STANDARD local time, i.e. the clock time with any
    daylight-saving (DST) hour removed. Example: China observed DST in 1986-1991, so a
    clock time of 12:00 in July 1988 is 11:00 standard time.
  * No longitude / "true solar time" adjustment (that is a separate, optional convention).
  * Historical non-DST offsets (e.g. Java used UTC+7:30 before 1964) are taken as entered:
    the clock time was the standard time of that era.
  * The lunar date and the two-hour block (shichen) are taken from the standard local
    date/time, so a DST hour can move a birth across midnight or across a block boundary.

Public functions:
    apply_birth_timezone(birth_date, birth_time, tz_name) -> (date, time, info)
    boundary_info(time, margin_minutes=15)                 -> dict or None
    render_timezone_select(st, lang)                       -> tz id   (inside the birth form)
    render_time_notes(st, lang)                            -> shows notes after the chart is built
"""
import datetime

try:
    from zoneinfo import ZoneInfo, available_timezones
except Exception:  # pragma: no cover
    ZoneInfo = None
    available_timezones = None

CURATED = [
    ("Asia/Jakarta", "Jakarta, Sumatra, Java (WIB)"),
    ("Asia/Makassar", "Bali, Sulawesi, Kalimantan (WITA)"),
    ("Asia/Jayapura", "Papua, Maluku (WIT)"),
    ("Asia/Singapore", "Singapore"),
    ("Asia/Kuala_Lumpur", "Malaysia"),
    ("Asia/Shanghai", "China"),
    ("Asia/Hong_Kong", "Hong Kong"),
    ("Asia/Taipei", "Taiwan"),
    ("Asia/Tokyo", "Japan"),
    ("Asia/Seoul", "Korea"),
    ("Asia/Bangkok", "Thailand"),
    ("Asia/Manila", "Philippines"),
    ("Asia/Dubai", "UAE"),
    ("Australia/Perth", "Perth"),
    ("Australia/Sydney", "Sydney"),
    ("Pacific/Auckland", "New Zealand"),
    ("Europe/London", "United Kingdom"),
    ("Europe/Amsterdam", "Netherlands"),
    ("Europe/Berlin", "Germany"),
    ("America/New_York", "US Eastern"),
    ("America/Chicago", "US Central"),
    ("America/Los_Angeles", "US Pacific"),
    ("America/Toronto", "Canada Eastern"),
]
DEFAULT_TZ = "Asia/Jakarta"

# ------------------------------------------------------------------ calculation


def apply_birth_timezone(birth_date: datetime.date, birth_time: datetime.time, tz_name: str):
    """Return (standard_date, standard_time, info). Never raises: on any problem the clock
    time is returned unchanged with info['problem'] set."""
    naive = datetime.datetime.combine(birth_date, datetime.time(birth_time.hour, birth_time.minute))
    info = {
        "tz": tz_name, "clock": naive.strftime("%Y-%m-%d %H:%M"), "standard": naive.strftime("%Y-%m-%d %H:%M"),
        "dst_minutes": 0, "gap": False, "ambiguous": False, "problem": None, "date_changed": False,
    }
    if ZoneInfo is None:
        info["problem"] = "zoneinfo unavailable"
        return birth_date, birth_time, info
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        info["problem"] = "unknown time zone"
        return birth_date, birth_time, info

    first = naive.replace(tzinfo=tz, fold=0)
    second = naive.replace(tzinfo=tz, fold=1)
    # a clock time that does not exist (spring-forward gap) does not survive a round trip via UTC
    utc = datetime.timezone.utc
    info["gap"] = first.astimezone(utc).astimezone(tz).replace(tzinfo=None) != naive
    # a clock time that happened twice (fall-back hour)
    info["ambiguous"] = (not info["gap"]) and first.utcoffset() != second.utcoffset()

    dst = first.dst() or datetime.timedelta(0)
    if dst < datetime.timedelta(0):
        dst = datetime.timedelta(0)   # "negative DST" zones (e.g. Europe/Dublin winter): not a DST hour to remove
    std = naive - dst
    info["dst_minutes"] = int(dst.total_seconds() // 60)
    info["standard"] = std.strftime("%Y-%m-%d %H:%M")
    info["date_changed"] = std.date() != naive.date()
    return std.date(), datetime.time(std.hour, std.minute), info


def boundary_info(t: datetime.time, margin_minutes: int = 15):
    """If the time is within `margin_minutes` of a two-hour block boundary (odd hours:
    23:00, 01:00, 03:00 ... 21:00), return {'minutes': n, 'boundary': 'HH:00'}; else None."""
    m = t.hour * 60 + t.minute
    best = None
    for h in range(1, 24, 2):
        b = h * 60
        diff = min(abs(m - b), 1440 - abs(m - b))
        if best is None or diff < best[0]:
            best = (diff, h)
    if best[0] <= margin_minutes:
        return {"minutes": best[0], "boundary": "%02d:00" % best[1]}
    return None


# ------------------------------------------------------------------ text

TX = {
    "en": {
        "tz_label": "Birth place time zone",
        "dst": "Daylight saving time was in effect at birth, so your clock time {clock} was converted to standard time {std} for the chart.",
        "date": "This also moved the birth date to {date}.",
        "gap": "That clock time did not exist at the daylight-saving change in this time zone. Please check the birth time.",
        "ambiguous": "That clock time happened twice at the daylight-saving change. The first occurrence was used.",
        "boundary": "Your birth time is within {n} minutes of {b}, where the two-hour block changes. A small error in the time could change the chart.",
        "problem": "The time zone could not be applied, so the clock time was used as entered.",
    },
    "id": {
        "tz_label": "Zona waktu tempat lahir",
        "dst": "Waktu musim panas (DST) berlaku saat Anda lahir, sehingga jam {clock} diubah menjadi waktu standar {std} untuk bagan.",
        "date": "Ini juga memindahkan tanggal lahir menjadi {date}.",
        "gap": "Jam tersebut tidak ada pada saat perubahan waktu musim panas di zona waktu ini. Mohon periksa waktu lahir.",
        "ambiguous": "Jam tersebut terjadi dua kali pada saat perubahan waktu musim panas. Kejadian pertama yang digunakan.",
        "boundary": "Waktu lahir Anda berjarak {n} menit dari {b}, saat blok dua jam berganti. Kesalahan kecil pada waktu dapat mengubah bagan.",
        "problem": "Zona waktu tidak dapat diterapkan, jadi jam digunakan seperti yang dimasukkan.",
    },
    "zh": {
        "tz_label": "出生地時區",
        "dst": "您出生時當地實行夏令時間，因此排盤時已將鐘面時間 {clock} 換算為標準時間 {std}。",
        "date": "這也使出生日期變為 {date}。",
        "gap": "該時區在夏令時間轉換時沒有這個鐘面時間，請確認出生時間。",
        "ambiguous": "該鐘面時間在夏令時間轉換時出現兩次，已採用第一次。",
        "boundary": "您的出生時間距離 {b}（時辰交界）只有 {n} 分鐘，時間若有小誤差，命盤可能不同。",
        "problem": "無法套用時區，已按輸入的鐘面時間排盤。",
    },
}


def _tx(lang):
    return TX.get(lang, TX["en"])


# ------------------------------------------------------------------ Streamlit helpers


def _options():
    ids = [i for i, _ in CURATED]
    rest = []
    if available_timezones is not None:
        try:
            rest = sorted(z for z in available_timezones() if z not in ids and "/" in z and not z.startswith(("Etc/", "posix", "right")))
        except Exception:
            rest = []
    return ids + rest


def render_timezone_select(st, lang):
    options = _options()
    labels = dict(CURATED)
    browser_tz = None
    try:
        browser_tz = st.context.timezone
    except Exception:
        pass
    default = browser_tz if browser_tz in options else DEFAULT_TZ
    idx = options.index(default) if default in options else 0
    return st.selectbox(
        _tx(lang)["tz_label"], options, index=idx, key="birth_tz",
        format_func=lambda z: "%s - %s" % (labels[z], z) if z in labels else z,
    )


def make_notes(info, std_time, lang):
    """List of note strings for a computed info dict."""
    T = _tx(lang)
    notes, warns = [], []
    if info.get("problem"):
        warns.append(T["problem"])
    if info.get("dst_minutes"):
        notes.append(T["dst"].format(clock=info["clock"][11:], std=info["standard"][11:]))
        if info.get("date_changed"):
            notes.append(T["date"].format(date=info["standard"][:10]))
    if info.get("gap"):
        warns.append(T["gap"])
    if info.get("ambiguous"):
        notes.append(T["ambiguous"])
    b = boundary_info(std_time)
    if b:
        warns.append(T["boundary"].format(n=b["minutes"], b=b["boundary"]))
    return notes, warns


def store_time_info(st, info, std_time):
    st.session_state["time_info"] = {"info": info, "std_hour": std_time.hour, "std_minute": std_time.minute}


def render_time_notes(st, lang):
    data = st.session_state.get("time_info")
    if not data:
        return
    notes, warns = make_notes(data["info"], datetime.time(data["std_hour"], data["std_minute"]), lang)
    for n in notes:
        st.caption(n)
    for w in warns:
        st.warning(w)
