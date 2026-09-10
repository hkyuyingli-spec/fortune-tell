from __future__ import annotations


class ZiWeiChart:
    """Minimal compatibility layer for the current workspace snapshot.

    This intentionally provides enough structure for the Streamlit UI to load and
    render a placeholder Zi Wei chart when the full engine modules are absent.
    """

    def __init__(self, birth_chart, gender):
        self.birth_chart = birth_chart
        self.gender = gender
        self.bureau_number = 5
        self.soul_p = "命宮"
        self.decades_by_p = {
            "命宮": {"range": [0, 9]},
            "兄弟宮": {"range": [10, 19]},
            "夫妻宮": {"range": [20, 29]},
            "子女宮": {"range": [30, 39]},
            "財帛宮": {"range": [40, 49]},
            "疾厄宮": {"range": [50, 59]},
            "遷移宮": {"range": [60, 69]},
            "交友宮": {"range": [70, 79]},
            "官祿宮": {"range": [80, 89]},
            "田宅宮": {"range": [90, 99]},
            "福德宮": {"range": [100, 109]},
            "父母宮": {"range": [110, 119]},
        }

    def palace_table(self):
        palaces = [
            ("命宮", "甲", "子", ["紫微", "天府"], "命主與身主的核心落點。", "此宮影響你如何定義自身方向與生涯主軸。"),
            ("兄弟宮", "乙", "丑", ["天機"], "兄弟與同輩關係。", "此宮反映你在人際網絡中的接觸方式與競爭感。"),
            ("夫妻宮", "丙", "寅", ["天相"], "婚姻與伴侶關係。", "此宮可讓你觀察伴侶型態與情感互動模式。"),
            ("子女宮", "丁", "卯", ["天梁"], "子女與教養方向。", "此宮關注你照顧他人、傳承價值的方式。"),
            ("財帛宮", "戊", "辰", ["武曲"], "財運與資源管理。", "此宮能幫你看待收入、安全感與有形資產。"),
            ("疾厄宮", "己", "巳", ["太陽"], "健康與體質。", "此宮提醒你注意身體節奏與休養方式。"),
            ("遷移宮", "庚", "午", ["天同"], "旅行、工作流動與環境變化。", "此宮反映你對新環境的適應與成長。"),
            ("交友宮", "辛", "未", ["廉貞"], "朋友與支持系統。", "此宮有助於觀察你如何結交人脈與尋求支持。"),
            ("官祿宮", "壬", "申", ["天府"], "事業與職場定位。", "此宮是工作能力、職業方向與貢獻感的窗口。"),
            ("田宅宮", "癸", "酉", ["巨門"], "居住、家族與資產。", "此宮能看出你對穩定感與居住環境的需求。"),
            ("福德宮", "甲", "戌", ["文昌"], "福祉與內在安定。", "此宮關係到你內在的幸福感與價值感。"),
            ("父母宮", "乙", "亥", ["文曲"], "父母與家庭教育。", "此宮反映你對家族關係與支持系統的感受。"),
        ]

        rows = []
        for palace, stem, branch, stars, meaning, blurb in palaces:
            rows.append(
                {
                    "palace": palace,
                    "stem": stem,
                    "branch": branch,
                    "stars": stars,
                    "meaning": meaning,
                    "blurb": blurb,
                }
            )
        return rows
