# Templated interpretation content keyed off real chart data, in three
# languages. This is structured/templated text (like Click108's own
# interpretations), not a claim of scientific validity. en/id are
# functional translations -- worth a native-speaker pass before this
# faces a real paying audience, especially id (the actual target market;
# see earlier market research on the Indonesian weton/primbon gap).

DAY_MASTER_BLURB = {
    "甲": {"zh": "像一棵挺立的大樹：正直、有領導欲，喜歡開創局面，但有時稍嫌固執。",
           "en": "Like a tall standing tree: upright, drawn to leadership, likes to pioneer new ground, but can be stubborn.",
           "id": "Seperti pohon besar yang berdiri tegak: jujur, punya jiwa kepemimpinan, suka merintis hal baru, tapi kadang keras kepala."},
    "乙": {"zh": "像柔韌的花草：適應力強、心思細膩，善於在複雜關係中找到生存空間。",
           "en": "Like flexible grass or flowers: highly adaptable, thoughtful, good at finding space to thrive within complex relationships.",
           "id": "Seperti tanaman yang lentur: sangat adaptif, penuh perasaan, pandai mencari ruang di tengah hubungan yang rumit."},
    "丙": {"zh": "像太陽：熱情外向、行動力強，天生的焦點人物，但耐性有待磨練。",
           "en": "Like the sun: warm, outgoing, high energy, a natural center of attention — but patience needs work.",
           "id": "Seperti matahari: hangat, terbuka, energik, secara alami jadi pusat perhatian — tapi kesabaran perlu dilatih."},
    "丁": {"zh": "像燭火：溫暖細緻、重感情，善於在小範圍內發揮深刻的影響力。",
           "en": "Like a candle flame: warm, detail-oriented, deeply relational, capable of profound influence in a small circle.",
           "id": "Seperti nyala lilin: hangat, teliti, sangat menghargai hubungan, mampu memberi pengaruh mendalam dalam lingkup kecil."},
    "戊": {"zh": "像高山：穩重可靠、責任感重，是團隊中值得信賴的支柱。",
           "en": "Like a mountain: steady, reliable, strong sense of responsibility — the pillar others lean on.",
           "id": "Seperti gunung: stabil, dapat diandalkan, tanggung jawab tinggi — menjadi tumpuan bagi orang lain."},
    "己": {"zh": "像田地：包容務實、善於培養他人，安全感需求較高。",
           "en": "Like farmland: accommodating, practical, good at nurturing others, with a higher need for security.",
           "id": "Seperti lahan pertanian: bisa menampung, praktis, pandai membina orang lain, tapi butuh rasa aman yang lebih tinggi."},
    "庚": {"zh": "像刀劍：果斷剛毅、原則性強，行事直接，不擅長拐彎抹角。",
           "en": "Like a blade: decisive, firm, strongly principled, direct in action — not built for beating around the bush.",
           "id": "Seperti pedang: tegas, kuat, berpegang pada prinsip, langsung dalam bertindak — tidak suka berbasa-basi."},
    "辛": {"zh": "像珠寶：講究細節、追求完美，對自己與他人要求都不低。",
           "en": "Like a gem: detail-oriented, perfectionistic, holds both self and others to high standards.",
           "id": "Seperti perhiasan: memperhatikan detail, perfeksionis, menuntut standar tinggi baik untuk diri sendiri maupun orang lain."},
    "壬": {"zh": "像江河：聰明善變、視野開闊，喜歡自由，不受拘束。",
           "en": "Like a river: clever, adaptable, broad-minded, values freedom and dislikes being constrained.",
           "id": "Seperti sungai: cerdas, mudah beradaptasi, berpikiran luas, menghargai kebebasan dan tidak suka dikekang."},
    "癸": {"zh": "像雨露：溫和內斂、直覺敏銳，善於體察他人情緒。",
           "en": "Like dew: gentle, reserved, sharply intuitive, attuned to other people's emotions.",
           "id": "Seperti embun: lembut, tenang, intuisi tajam, peka terhadap perasaan orang lain."},
}

MAJOR_STAR_BLURB = {
    "紫微": {"zh": "領導格局，重視地位與尊嚴，天生带著一種「帝王氣」，喜歡掌控大局。",
             "en": "A leadership pattern — values status and dignity, carries a natural \"commanding presence,\" likes being in control of the big picture.",
             "id": "Pola kepemimpinan — menghargai status dan martabat, memiliki \"aura pemimpin\" alami, suka mengendalikan gambaran besar."},
    "天機": {"zh": "腦筋轉得快，善謀略、點子多，但也容易多想，情緒隨思緒起伏。",
             "en": "A quick, strategic mind full of ideas — but prone to overthinking, with moods that rise and fall with the thoughts.",
             "id": "Pikiran cepat dan strategis, penuh ide — tapi cenderung terlalu banyak berpikir, suasana hati naik turun mengikuti pikiran."},
    "太陽": {"zh": "光明磊落、熱心公益，付出型人格，格外在意是否「被看見」。",
             "en": "Open and upright, community-minded, a giving personality — but especially sensitive to whether that giving is \"seen.\"",
             "id": "Terbuka dan jujur, peduli pada kepentingan bersama, kepribadian yang suka memberi — tapi sangat peka apakah usahanya \"terlihat\"."},
    "武曲": {"zh": "務實剛毅，執行力強，是天生的財務與行動派，情感表達較內斂。",
             "en": "Practical and firm, strong execution — a natural at finance and action, though emotional expression stays reserved.",
             "id": "Praktis dan tegas, eksekusi kuat — alami dalam hal keuangan dan tindakan, meski ekspresi emosinya cenderung tertutup."},
    "天同": {"zh": "溫和知足，重視生活品質與情感和諧，抗壓性需要後天培養。",
             "en": "Gentle and content, values quality of life and emotional harmony — stress tolerance is something to build over time.",
             "id": "Lembut dan mudah puas, menghargai kualitas hidup dan keharmonisan emosi — ketahanan terhadap tekanan perlu dilatih."},
    "廉貞": {"zh": "個性複雜多面，理性與感性交織，桃花與事業心並存。",
             "en": "A complex, many-sided personality where logic and emotion intertwine — romantic charm and career drive coexist.",
             "id": "Kepribadian kompleks dan berlapis, logika dan emosi saling terkait — daya tarik asmara dan ambisi karier berjalan bersamaan."},
    "天府": {"zh": "穩重厚道，善於守成與理財，是可靠的「大管家」型人物。",
             "en": "Steady and generous, good at preserving and managing resources — the reliable \"household steward\" type.",
             "id": "Stabil dan murah hati, pandai menjaga dan mengelola sumber daya — tipe \"pengurus rumah tangga\" yang dapat diandalkan."},
    "太陰": {"zh": "細膩內斂，重視家庭與內在世界，情感豐富但不輕易外露。",
             "en": "Subtle and reserved, values family and the inner world — emotionally rich but slow to show it.",
             "id": "Halus dan tertutup, menghargai keluarga dan dunia batin — kaya emosi tapi jarang menunjukkannya."},
    "貪狼": {"zh": "多才多藝、社交手腕靈活，慾望與才華並重，人生選項多。",
             "en": "Versatile and socially agile — ambition and talent in equal measure, with many possible paths in life.",
             "id": "Serbabisa dan lincah secara sosial — ambisi dan bakat seimbang, dengan banyak kemungkinan jalan hidup."},
    "巨門": {"zh": "口才犀利、分析力強，適合靠語言、專業吃飯，也容易因言惹議。",
             "en": "Sharp-tongued and analytical — well suited to work built on language or expertise, though words can also stir controversy.",
             "id": "Tajam bicara dan analitis — cocok untuk pekerjaan berbasis bahasa atau keahlian, meski perkataan bisa memicu kontroversi."},
    "天相": {"zh": "溫和公正，重視形象與服務精神，是天生的協調者。",
             "en": "Gentle and fair, values image and a spirit of service — a natural mediator.",
             "id": "Lembut dan adil, menghargai citra dan semangat melayani — seorang mediator alami."},
    "天梁": {"zh": "老成持重，樂於照顧他人，常扮演長輩或貴人的角色。",
             "en": "Mature and steady, happy to look after others — often the elder or benefactor figure in a room.",
             "id": "Dewasa dan stabil, senang mengurus orang lain — sering berperan sebagai sosok tetua atau penolong."},
    "七殺": {"zh": "行動派、敢衝敢拚，人生起伏較大，適合開創型事業。",
             "en": "A bold doer, willing to charge ahead — life tends to have bigger swings, well suited to pioneering ventures.",
             "id": "Pelaku yang berani, siap maju terus — kehidupan cenderung lebih naik turun, cocok untuk usaha rintisan."},
    "破軍": {"zh": "破舊立新、不安於現狀，變動與挑戰是這個格局的常態。",
             "en": "Breaks the old to build the new, restless with the status quo — change and challenge are the norm for this pattern.",
             "id": "Menghancurkan yang lama demi membangun yang baru, gelisah dengan keadaan saat ini — perubahan dan tantangan adalah hal biasa bagi pola ini."},
}

BUREAU_BLURB = {
    "水": {"zh": "水二局：人生節奏偏快起步，早年較早經歷變動與磨練。",
           "en": "Water Bureau (2): life tends to start at a faster pace, with change and challenge arriving earlier than usual.",
           "id": "Biro Air (2): hidup cenderung dimulai dengan lebih cepat, perubahan dan tantangan datang lebih awal dari biasanya."},
    "木": {"zh": "木三局：成長節奏中庸，穩紮穩打型的人生曲線。",
           "en": "Wood Bureau (3): a moderate growth pace — a steady, step-by-step life curve.",
           "id": "Biro Kayu (3): laju pertumbuhan sedang — kurva hidup yang stabil dan bertahap."},
    "金": {"zh": "金四局：性格中帶著一份韌性，需要時間淬鍊才能顯出光芒。",
           "en": "Metal Bureau (4): a resilient core that needs time under pressure before it truly shines.",
           "id": "Biro Logam (4): memiliki ketahanan yang perlu waktu dan tekanan sebelum benar-benar bersinar."},
    "土": {"zh": "土五局：大器晚成的格局，中年之後的發展往往更為扎實。",
           "en": "Earth Bureau (5): a \"late bloomer\" pattern — development after mid-life tends to be the most solid.",
           "id": "Biro Tanah (5): pola \"berkembang belakangan\" — perkembangan setelah usia pertengahan cenderung paling kokoh."},
    "火": {"zh": "火六局：人生起伏較為明顯，需要學習在高峰與低谷間找到平衡。",
           "en": "Fire Bureau (6): more pronounced ups and downs — the lesson is finding balance between the peaks and the valleys.",
           "id": "Biro Api (6): naik turun yang lebih terasa — pelajarannya adalah menemukan keseimbangan antara puncak dan lembah."},
}

PALACE_MEANING = {
    "命宮": {"zh": "你的核心性格與人生基調", "en": "Your core personality and life's underlying tone", "id": "Kepribadian inti dan nada dasar kehidupan Anda"},
    "兄弟": {"zh": "手足情誼與合夥關係", "en": "Sibling bonds and partnerships", "id": "Ikatan saudara dan hubungan kemitraan"},
    "夫妻": {"zh": "感情觀與婚姻狀態", "en": "Outlook on love and marriage", "id": "Pandangan tentang cinta dan pernikahan"},
    "子女": {"zh": "子女緣分與創造力", "en": "Connection with children and creativity", "id": "Hubungan dengan anak dan kreativitas"},
    "財帛": {"zh": "賺錢方式與金錢觀", "en": "How you earn and relate to money", "id": "Cara memperoleh dan memandang uang"},
    "疾厄": {"zh": "健康體質與壓力反應", "en": "Health constitution and stress response", "id": "Kondisi kesehatan dan respons terhadap stres"},
    "遷移": {"zh": "外出運與人際際遇", "en": "Fortune while away from home and social encounters", "id": "Keberuntungan saat bepergian dan pertemuan sosial"},
    "交友": {"zh": "朋友圈與人脈資源", "en": "Friend circle and network resources", "id": "Lingkaran pertemanan dan jaringan relasi"},
    "官祿": {"zh": "事業發展與職場定位", "en": "Career development and professional positioning", "id": "Perkembangan karier dan posisi profesional"},
    "田宅": {"zh": "不動產運與居家生活", "en": "Property fortune and home life", "id": "Keberuntungan properti dan kehidupan rumah tangga"},
    "福德": {"zh": "精神生活與福氣厚薄", "en": "Inner/spiritual life and depth of good fortune", "id": "Kehidupan batin/spiritual dan kedalaman keberuntungan"},
    "父母": {"zh": "與父母長輩的緣分", "en": "Connection with parents and elders", "id": "Hubungan dengan orang tua dan sesepuh"},
}

_LABELS = {
    "your_pillars": {"zh": "你的四柱八字", "en": "Your Four Pillars (BaZi)", "id": "Empat Pilar Anda (BaZi)"},
    "day_master": {"zh": "日主（代表你自己）", "en": "Day Master (represents you)", "id": "Day Master (mewakili diri Anda)"},
    "life_palace": {"zh": "命宮", "en": "Life Palace", "id": "Istana Kehidupan"},
    "main_star_is": {"zh": "主星為", "en": "main star(s):", "id": "bintang utama:"},
    "no_main_star": {"zh": "（本宮無主星，個性受對宮及三方影響較大）", "en": "(no major star here — personality is shaped more by the opposite and triangle palaces)",
                      "id": "(tidak ada bintang utama di sini — kepribadian lebih dipengaruhi istana berhadapan dan segitiga)"},
    "ming_shen_zhu": {"zh": "命主 / 身主", "en": "Life Star / Body Star", "id": "Bintang Kehidupan / Bintang Tubuh"},
    "bureau": {"zh": "五行局", "en": "Five-Element Bureau", "id": "Biro Lima Elemen"},
    "life_star_reading": {"zh": "命宮主星解讀", "en": "Life Palace star reading", "id": "Pembacaan bintang Istana Kehidupan"},
    "no_star_generic": {"zh": "無主星", "en": "no major star", "id": "tanpa bintang utama"},
    "no_star_blurb": {"zh": "此宮由對宮及三方四正的星曜影響較大，建議合併命宮一起看。",
                       "en": "This palace is shaped more by the opposite and triangle palaces' stars — best read together with the Life Palace.",
                       "id": "Istana ini lebih dipengaruhi oleh bintang dari istana berhadapan dan segitiga — sebaiknya dibaca bersama Istana Kehidupan."},
}


def free_tier_summary(bazi_pillars, day_master, ziwei, lang="zh"):
    life_row = ziwei.palace_table()[0]
    star_text = "、".join(life_row["stars"]) if life_row["stars"] else _LABELS["no_main_star"][lang]
    day_stem = bazi_pillars["day"][0]
    L = {k: v[lang] for k, v in _LABELS.items()}
    lines = [
        f"**{L['your_pillars']}**：{bazi_pillars['year']} {bazi_pillars['month']} {bazi_pillars['day']} {bazi_pillars['hour']}",
        f"**{L['day_master']}**：{day_stem} — {DAY_MASTER_BLURB.get(day_stem, {}).get(lang, '')}",
        f"**{L['life_palace']}**：{life_row['stem']}{life_row['branch']}，{L['main_star_is']} {star_text}",
        f"**{L['ming_shen_zhu']}**：{ziwei.ming_zhu} / {ziwei.shen_zhu}",
        f"**{L['bureau']}**：{ziwei.bureau_name} — {BUREAU_BLURB.get(ziwei.bureau_element, {}).get(lang, '')}",
    ]
    if life_row["stars"]:
        lines.append(f"**{L['life_star_reading']}**：" + " ".join(MAJOR_STAR_BLURB.get(s, {}).get(lang, "") for s in life_row["stars"]))
    return "\n\n".join(lines)


def paid_tier_report(ziwei, current_year=None, lang="zh"):
    rows = ziwei.palace_table()
    out = []
    for row in rows:
        stars = "、".join(row["stars"]) if row["stars"] else _LABELS["no_star_generic"][lang]
        blurb = " ".join(MAJOR_STAR_BLURB.get(s, {}).get(lang, "") for s in row["stars"]) or _LABELS["no_star_blurb"][lang]
        body_tag = ""
        if row["is_body_palace"]:
            body_tag = {"zh": "（身宮）", "en": " (Body Palace)", "id": " (Istana Tubuh)"}[lang]
        d_start, d_end = row["decade"]["range"]
        suffix = "歲" if lang == "zh" else "" if lang == "en" else " tahun"
        out.append({
            "palace": row["palace"] + body_tag,
            "meaning": PALACE_MEANING.get(row["palace"], {}).get(lang, ""),
            "stem_branch": row["stem"] + row["branch"],
            "stars": stars,
            "blurb": blurb,
            "decade_range": f"{d_start}–{d_end}{suffix}",
        })
    current_palace = ziwei.current_year_palace(current_year) if current_year else None
    return out, current_palace
