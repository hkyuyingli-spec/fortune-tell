"""Run: python test_time_engine.py   (needs time_engine.py, calendar_engine.py, ziwei_engine.py)"""
import datetime as dt
import time_engine as te
from calendar_engine import BirthChart

D, T = dt.date, dt.time
def run(y, m, d, h, mi, tz):
    sd, st, info = te.apply_birth_timezone(D(y, m, d), T(h, mi), tz)
    return sd, st, info

# 1. China had daylight saving 1986-1991: clock 12:00 in July 1988 is 11:00 standard time
sd, st, i = run(1988, 7, 1, 12, 0, "Asia/Shanghai")
assert (sd, st) == (D(1988, 7, 1), T(11, 0)) and i["dst_minutes"] == 60, (sd, st, i)
# 2. same place, winter: no change
sd, st, i = run(1988, 12, 1, 12, 0, "Asia/Shanghai")
assert (sd, st) == (D(1988, 12, 1), T(12, 0)) and i["dst_minutes"] == 0
# 3. China without DST (e.g. 2005): no change
assert run(2005, 7, 1, 12, 0, "Asia/Shanghai")[:2] == (D(2005, 7, 1), T(12, 0))
# 4. Indonesia has no daylight saving: no change, any date
for y in (1950, 1975, 1990, 2020):
    sd, st, i = run(y, 7, 1, 23, 30, "Asia/Jakarta")
    assert (sd, st) == (D(y, 7, 1), T(23, 30)) and i["dst_minutes"] == 0
# 5. DST can move a birth across midnight: New York 4 Jul 2020 00:30 (DST) = 3 Jul 23:30 standard
sd, st, i = run(2020, 7, 4, 0, 30, "America/New_York")
assert (sd, st) == (D(2020, 7, 3), T(23, 30)) and i["date_changed"]
# 6. Negative-DST zone (Dublin winter) must NOT be shifted
sd, st, i = run(2021, 1, 15, 12, 0, "Europe/Dublin")
assert (sd, st) == (D(2021, 1, 15), T(12, 0)) and i["dst_minutes"] == 0
# 7. spring-forward gap (clock time that never existed) and fall-back repeat
assert run(2021, 3, 14, 2, 30, "America/New_York")[2]["gap"] is True
assert run(2021, 11, 7, 1, 30, "America/New_York")[2]["ambiguous"] is True
assert run(2021, 6, 1, 12, 0, "America/New_York")[2]["gap"] is False
# 8. bad time zone never crashes
sd, st, i = run(1990, 1, 1, 12, 0, "Nowhere/Land")
assert (sd, st) == (D(1990, 1, 1), T(12, 0)) and i["problem"]
# 9. boundary warning (blocks change at odd hours)
assert te.boundary_info(T(22, 55))["boundary"] == "23:00" and te.boundary_info(T(22, 55))["minutes"] == 5
assert te.boundary_info(T(0, 58))["boundary"] == "01:00"
assert te.boundary_info(T(12, 0)) is None            # middle of a block: no warning
assert te.boundary_info(T(12, 59))["boundary"] == "13:00" and te.boundary_info(T(12, 59))["minutes"] == 1
assert te.boundary_info(T(11, 5))["boundary"] == "11:00"
# 10. end to end: Shanghai 1 Jul 1988 00:30 (DST) -> standard 30 Jun 23:30 = late-night Zi on 30 June
sd, st, i = run(1988, 7, 1, 0, 30, "Asia/Shanghai")
bc = BirthChart(sd.year, sd.month, sd.day, st.hour, st.minute)
assert (sd, st) == (D(1988, 6, 30), T(23, 30)) and bc.is_late_zi and bc.solar_day == 30
# 11. notes text exists in all three languages
for lg in ("en", "id", "zh"):
    notes, _ = te.make_notes(i, st, lg)                 # DST note (+ date-change note)
    assert len(notes) == 2, (lg, notes)
    _, warns = te.make_notes(i, T(22, 55), lg)           # boundary warning
    assert len(warns) == 1, (lg, warns)
print("All time_engine tests passed (11 checks).")
