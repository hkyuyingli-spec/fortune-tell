from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart

cases = [
    dict(y=1990, mo=8, d=15, h=12, gender="male"),   # 午时(11-13) -> use hour=12
    dict(y=1985, mo=2, d=4, h=0, gender="female"),    # 子时, right on the 立春 boundary day
    dict(y=2000, mo=1, d=1, h=22, gender="male"),     # 亥时(21-23) -> use hour=22
]

for c in cases:
    bc = BirthChart(c["y"], c["mo"], c["d"], c["h"])
    zw = ZiWeiChart(bc, c["gender"])
    print(f"===== {c['y']}-{c['mo']:02d}-{c['d']:02d} h={c['h']} {c['gender']} =====")
    print("four pillars:", bc.four_pillars.as_dict())
    print("lunar month (zi wei):", bc.zi_wei_month_number(), "lunar day:", bc.lunar_day, "leap:", bc.is_leap_month)
    print("life palace:", zw.soul_stem + zw.soul_branch, " body palace branch:", chr(0) )
    print("bureau:", zw.bureau_name)
    for row in zw.palace_table():
        print(f"  {row['palace']:4s} {row['stem']}{row['branch']}  stars={','.join(row['stars']) or '-':20s} body={row['is_body_palace']} decade={row['decade']['range']}")
    print()
