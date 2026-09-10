from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class FourPillars:
    year: tuple[str, str]
    month: tuple[str, str]
    day: tuple[str, str]
    time: tuple[str, str]

    def as_dict(self):
        return {
            "year": list(self.year),
            "month": list(self.month),
            "day": list(self.day),
            "time": list(self.time),
        }


class BirthChart:
    """Minimal compatibility layer for the current workspace snapshot.

    The full project files referenced by README.md are not present here, so this
    provides the small surface area needed for the app to import and render a
    sensible default chart structure.
    """

    def __init__(self, year, month, day, hour=0, minute=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.datetime = datetime(year, month, day, hour, minute)

        # Deterministic placeholder pillars so the UI can render immediately.
        self.four_pillars = FourPillars(
            year=("甲", "子"),
            month=("乙", "丑"),
            day=("丙", "寅"),
            time=("丁", "卯"),
        )
