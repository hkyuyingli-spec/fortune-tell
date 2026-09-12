"""
UI string translations. Content translations (star meanings, day-master
blurbs, etc.) live in interpretation.py's per-language dictionaries --
this module is just the app chrome (labels, buttons, captions).

Coverage note: zh is the original, carefully-worded version. en and id
are functional translations aimed at correctness and usability, not
polished native copywriting -- worth a native-speaker pass before this
is shown to a real paying audience, especially id since that's the
actual target market this was built for (see earlier market research).
"""

LANGS = {"zh": "中文", "en": "English", "id": "Bahasa Indonesia"}

STRINGS = {
    "app_title": {"zh": "命盤 · Destiny Chart", "en": "Destiny Chart", "id": "Destiny Chart"},
    "app_caption": {
        "zh": "紫微斗數 + 八字 命盤產生器 — 免費看命盤結構，付費解鎖完整解讀",
        "en": "Zi Wei Dou Shu + BaZi chart generator — free structure, unlock the full reading",
        "id": "Generator bagan Zi Wei Dou Shu + BaZi — struktur gratis, buka pembacaan lengkap",
    },
    "know_time_q": {
        "zh": "你知道確切的出生時間嗎？",
        "en": "Do you know your exact birth time?",
        "id": "Apakah Anda tahu waktu lahir Anda secara pasti?",
    },
    "know_time_yes": {"zh": "✅ 我知道確切的出生時間", "en": "✅ Yes, I know my exact birth time", "id": "✅ Ya, saya tahu waktu lahir pasti"},
    "know_time_no": {"zh": "❓ 我不確定 / 不知道出生時間", "en": "❓ I'm not sure / don't know", "id": "❓ Saya tidak yakin / tidak tahu"},
    "birth_date": {"zh": "出生日期（陽曆）", "en": "Birth date (solar calendar)", "id": "Tanggal lahir (kalender masehi)"},
    "birth_time": {"zh": "出生時間", "en": "Birth time", "id": "Waktu lahir"},
    "gender": {"zh": "性別", "en": "Gender", "id": "Jenis kelamin"},
    "male": {"zh": "男", "en": "Male", "id": "Laki-laki"},
    "female": {"zh": "女", "en": "Female", "id": "Perempuan"},
    "reveal_btn": {"zh": "排盤 Reveal Chart", "en": "Reveal Chart", "id": "Tampilkan Bagan"},
    "free_tier_header": {"zh": "免費 · 命盤概覽", "en": "Free · Chart Overview", "id": "Gratis · Ringkasan Bagan"},
    "unlock_info": {
        "zh": "完整報告包含：十二宮完整星曜、每個宮位解讀、十年大限排程、今年流年宮位",
        "en": "Full report includes: all 12 palaces' stars, per-palace interpretation, the 10-year decade cycle, and this year's palace",
        "id": "Laporan lengkap mencakup: bintang di 12 istana, interpretasi tiap istana, siklus 10 tahun, dan istana tahun ini",
    },
    "unlock_btn": {"zh": "🔓 解鎖完整報告 Unlock Full Report", "en": "🔓 Unlock Full Report", "id": "🔓 Buka Laporan Lengkap"},
    "paid_tier_header": {"zh": "付費 · 完整命盤解讀", "en": "Full Reading", "id": "Pembacaan Lengkap"},
    "current_year_palace": {"zh": "年流年宮位：", "en": " current-year palace: ", "id": " istana tahun ini: "},
    "decade_label": {"zh": "大限：", "en": "Decade: ", "id": "Dekade: "},
    "years_suffix": {"zh": "歲", "en": "", "id": " tahun"},
    "disclaimer": {
        "zh": "此命盤結構（十二宮、十四主星、五行局、大限）依紫微斗數傳統排盤規則計算，並經過與開源排盤工具（iztro）交叉驗證。目前尚未納入輔星、四化飛星與逐月/逐日流曜，屬於下一階段功能。本報告僅供自我探索與參考，非科學預測，請勿作為人生重大決策的唯一依據。",
        "en": "This chart's structure (12 palaces, 14 major stars, five-element bureau, decade cycles) is computed using traditional Zi Wei Dou Shu rules and cross-validated against an open-source reference implementation (iztro). Auxiliary stars, the Four Transformations, and month/day-level overlays aren't included yet. This report is for self-reflection only, not a scientific prediction — please don't use it as your sole basis for major life decisions.",
        "id": "Struktur bagan ini (12 istana, 14 bintang utama, elemen lima unsur, siklus dekade) dihitung menggunakan aturan tradisional Zi Wei Dou Shu dan divalidasi silang dengan implementasi referensi open-source (iztro). Bintang tambahan, Empat Transformasi, dan overlay bulanan/harian belum termasuk. Laporan ini hanya untuk refleksi diri, bukan prediksi ilmiah — jangan jadikan satu-satunya dasar keputusan besar dalam hidup Anda.",
    },
    "rect_intro": {
        "zh": "紫微斗數的命宮、身宮、十四主星都是由「出生時辰」直接決定的 —— 沒有時辰，命盤不是「比較不準」，而是無法唯一決定：同一天出生、不同時辰，可能對應到完全不同的命盤。以下用傳統「定盤」的方式，透過幾個問題幫你縮小範圍。",
        "en": "The life palace, body palace, and 14 major stars are all directly determined by birth TIME — without it, the chart isn't \"less accurate\", it's genuinely undetermined: the same birth date at a different hour can produce a completely different chart. Below, we use the traditional \"rectification\" approach — a few questions to narrow it down.",
        "id": "Istana kehidupan, istana tubuh, dan 14 bintang utama semuanya ditentukan langsung oleh WAKTU lahir — tanpa itu, bagan bukan \"kurang akurat\", tapi benar-benar tidak dapat ditentukan: tanggal lahir yang sama pada jam berbeda bisa menghasilkan bagan yang sama sekali berbeda. Di bawah ini kami gunakan pendekatan tradisional \"rektifikasi\" — beberapa pertanyaan untuk mempersempit kemungkinan.",
    },
    "rect_start_btn": {"zh": "開始定盤 Start Rectification", "en": "Start Rectification", "id": "Mulai Rektifikasi"},
    "rect_step1_header": {"zh": "第一步：哪一段個性描述最像你？", "en": "Step 1: Which personality description fits you best?", "id": "Langkah 1: Deskripsi kepribadian mana yang paling cocok?"},
    "rect_step1_caption": {"zh": "選一個最接近的（不用完全符合，選最像的就好）", "en": "Pick the closest match (doesn't need to be perfect)", "id": "Pilih yang paling mendekati (tidak perlu sempurna)"},
    "rect_next_btn": {"zh": "下一步", "en": "Next", "id": "Lanjut"},
    "rect_step2_header": {"zh": "第二步：人生中一個明顯的轉折點，大概發生在幾歲？", "en": "Step 2: Roughly how old were you at a major life turning point?", "id": "Langkah 2: Kira-kira usia berapa saat titik balik besar dalam hidup Anda?"},
    "rect_step2_caption": {
        "zh": "例如：換跑道、重大決定、明顯的順逆變化。不確定的話可以按「跳過」。",
        "en": "e.g. a career change, a major decision, a clear turn for better or worse. If unsure, press Skip.",
        "id": "misalnya: ganti karier, keputusan besar, perubahan nasib yang jelas. Jika tidak yakin, tekan Lewati.",
    },
    "rect_age_label": {"zh": "大約年齡", "en": "Approximate age", "id": "Perkiraan usia"},
    "rect_confirm_age_btn": {"zh": "確認年齡", "en": "Confirm age", "id": "Konfirmasi usia"},
    "rect_skip_btn": {"zh": "跳過此題", "en": "Skip this question", "id": "Lewati pertanyaan ini"},
    "rect_no_narrow_note": {
        "zh": "這個年齡沒有幫助縮小範圍——你目前的候選時辰在這個年齡附近都沒有大限轉換，所以維持原本的名單。",
        "en": "That age didn't help narrow it down — none of your current candidates have a decade-cycle turn near that age, so the list is unchanged.",
        "id": "Usia itu tidak membantu mempersempit pilihan — tidak ada kandidat Anda yang memiliki pergantian siklus dekade di sekitar usia itu, jadi daftar tidak berubah.",
    },
    "rect_result_single": {"zh": "根據你的回答，最可能的時辰是：", "en": "Based on your answers, the most likely time is:", "id": "Berdasarkan jawaban Anda, waktu yang paling mungkin adalah:"},
    "rect_view_chart_btn": {"zh": "查看完整命盤", "en": "View Full Chart", "id": "Lihat Bagan Lengkap"},
    "rect_result_multi": {"zh": "縮小到 {n} 個可能的時辰，請憑直覺選一個最像你的：", "en": "Narrowed to {n} possible times — pick the one that feels most like you:", "id": "Dipersempit menjadi {n} kemungkinan waktu — pilih yang paling terasa seperti Anda:"},
    "rect_choose_label": {"zh": "選擇", "en": "Choose", "id": "Pilih"},
    "rect_confirm_choice_btn": {"zh": "確認選擇", "en": "Confirm choice", "id": "Konfirmasi pilihan"},
    "rect_restart_btn": {"zh": "重新開始定盤", "en": "Start Over", "id": "Mulai Ulang"},
    "rect_done_caption": {
        "zh": "以下命盤基於推定時辰：{label}（{time_range}）— 如未來確認實際時辰，結果可能不同。",
        "en": "This chart is based on the estimated time: {label} ({time_range}) — results may differ once you confirm your actual birth time.",
        "id": "Bagan ini berdasarkan waktu perkiraan: {label} ({time_range}) — hasil dapat berbeda setelah Anda memastikan waktu lahir sebenarnya.",
    },
    "rect_redo_btn": {"zh": "重新定盤", "en": "Redo Rectification", "id": "Ulangi Rektifikasi"},
    "ai_chat_header": {"zh": "💬 問AI · Ask about your chart", "en": "💬 Ask AI about your chart", "id": "💬 Tanya AI tentang bagan Anda"},
    "ai_not_configured": {
        "zh": "AI 問答尚未設定。需要在 Streamlit Cloud 的 App settings → Secrets 加入 GITHUB_TOKEN。",
        "en": "AI Q&A isn't set up yet. Add a GITHUB_TOKEN under App settings → Secrets in Streamlit Cloud.",
        "id": "Tanya jawab AI belum diatur. Tambahkan GITHUB_TOKEN di App settings → Secrets di Streamlit Cloud.",
    },
    "ai_chat_placeholder": {
        "zh": "問問你的命盤，例如：我適合創業嗎？我的財帛宮代表什麼？",
        "en": "Ask about your chart, e.g. Should I start a business? What does my wealth palace mean?",
        "id": "Tanyakan tentang bagan Anda, mis. Apakah saya cocok berbisnis? Apa arti istana kekayaan saya?",
    },
    "ai_thinking": {"zh": "思考中...", "en": "Thinking...", "id": "Sedang berpikir..."},
    "ai_category_header": {"zh": "或選一個你想了解的主題：", "en": "Or pick a topic you're curious about:", "id": "Atau pilih topik yang ingin Anda ketahui:"},
    "language_label": {"zh": "語言 / Language", "en": "Language", "id": "Bahasa"},
    "cat_wealth": {"zh": "💰 財富", "en": "💰 Wealth", "id": "💰 Kekayaan"},
    "cat_career": {"zh": "💼 事業", "en": "💼 Career", "id": "💼 Karier"},
    "cat_love": {"zh": "❤️ 感情", "en": "❤️ Love", "id": "❤️ Cinta"},
    "cat_property": {"zh": "🏠 置產", "en": "🏠 Property", "id": "🏠 Properti"},
    "cat_business": {"zh": "📈 創業", "en": "📈 Business", "id": "📈 Bisnis"},
    "cat_other": {"zh": "❓ 其他", "en": "❓ Other", "id": "❓ Lainnya"},
    "cat_q_wealth": {
        "zh": "請根據我的財帛宮，說明我的賺錢方式與金錢觀，還有需要注意的地方。",
        "en": "Based on my Wealth Palace, what does it suggest about how I earn money and my relationship with money — and what should I watch for?",
        "id": "Berdasarkan Istana Kekayaan saya, apa yang ditunjukkan tentang cara saya memperoleh uang dan hubungan saya dengan uang — dan apa yang perlu diperhatikan?",
    },
    "cat_q_career": {
        "zh": "請根據我的官祿宮，分析我適合的職業方向與事業發展重點。",
        "en": "Based on my Career Palace, what direction or focus would suit my career development?",
        "id": "Berdasarkan Istana Karier saya, arah atau fokus apa yang cocok untuk perkembangan karier saya?",
    },
    "cat_q_love": {
        "zh": "請根據我的夫妻宮，說明我的感情觀與婚姻狀態的可能傾向。",
        "en": "Based on my Marriage Palace, what does it suggest about my approach to love and relationships?",
        "id": "Berdasarkan Istana Pernikahan saya, apa yang ditunjukkan tentang pandangan saya terhadap cinta dan hubungan?",
    },
    "cat_q_property": {
        "zh": "請根據我的田宅宮，說明我的不動產運與居家生活傾向。",
        "en": "Based on my Property Palace, what does it suggest about property fortune and home life?",
        "id": "Berdasarkan Istana Properti saya, apa yang ditunjukkan tentang keberuntungan properti dan kehidupan rumah tangga saya?",
    },
    "cat_q_business": {
        "zh": "請根據我的官祿宮和財帛宮，分析我是否適合創業，以及需要注意什麼。",
        "en": "Based on my Career and Wealth Palaces, does my chart suggest I'm suited to starting a business, and what should I watch out for?",
        "id": "Berdasarkan Istana Karier dan Kekayaan saya, apakah bagan saya menunjukkan saya cocok memulai bisnis, dan apa yang perlu diperhatikan?",
    },
}


def t(key: str, lang: str = "zh", **kwargs) -> str:
    text = STRINGS.get(key, {}).get(lang) or STRINGS.get(key, {}).get("zh", key)
    return text.format(**kwargs) if kwargs else text
