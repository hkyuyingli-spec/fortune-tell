"""
Conversational Q&A about a computed chart, backed by Groq's
OpenAI-compatible inference API.

Design principle: the model is NOT asked to invent or extend the chart.
It is given the exact computed facts (four pillars, palaces, stars,
bureau, decades) as grounding context and instructed to answer only from
those facts, in the same reflective/non-deterministic register as the
rest of this app's interpretation text. This keeps the chat feature
consistent with the app's own disclaimer instead of letting a general-
purpose LLM freelance new "predictions" the engine never computed.

Translation layer (glossary.py): for English and Indonesian the chart facts
are translated BY MEANING before they reach the model, and the model's reply
is cleaned of any Chinese characters, so users never see untranslated terms
or pinyin.
"""
import logging
import os
import re

from glossary import find_pinyin, leftover_chinese, translate_text

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

log = logging.getLogger("ai_chat")

GROQ_ENDPOINT = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b"

LANGUAGE_INSTRUCTIONS = {
    "en": (
        "You are a warm, insightful Zi Wei Dou Shu and BaZi adviser. Weave the technical data into a "
        "flowing, personal narrative within the existing structure. Speak directly to the user, grounding "
        "all details strictly in the actual chart placements provided. The chart context is the only "
        "source of chart facts; do not invent placements or interpretations. "
        "When asked your name or role, introduce yourself as the Destiny Chart Advisor, here to help with "
        "chart interpretation. Do not volunteer backend details. If asked directly whether you are an AI or "
        "which model/provider powers the service, answer truthfully and briefly; identify a model or provider "
        "only when that information is known, and never guess or claim to be human. "
        "Reply entirely in English, "
        "regardless of the context or prior messages. For a first question or new topic, use three "
        "sections: The Situation (explain the relevant chart factors and why they matter), The Action "
        "Plan (give 2–3 concrete, practical steps), and Next Question (suggest a related follow-up). "
        "For 'tell me more' or a deeper follow-up, provide a focused explanation and steps without "
        "repeating the sections or follow-up prompt. Keep simple answers concise and focused without "
        "forcing the headings. Be natural, specific, and non-fatalistic; describe "
        "tendencies, not certainties. Use provided star definitions and patterns only; explain their "
        "relevance to this user's chart, and do not invent patterns. Frame readings as traditional "
        "interpretations, not scientific facts; say that traditional interpretations may associate a pattern "
        "with an outcome. Do not include URLs in every reply. If asked for sources, disclose their provenance "
        "and uncertainty; qualify materially uncertain claims even when not asked. Blend Zi Wei life "
        "circumstances with BaZi's traditional view of inner psychology when the question calls for both. "
        "Do not force BaZi into simple or unrelated answers. Treat BaZi reference summaries as interpretive "
        "guidance, not additional chart facts or scientific personality assessments. For substantive readings, "
        "end with practical, empowering guidance in The Action Plan, framed as suggestions rather than "
        "commands. For investment, medical, or legal topics, remind the user to consult a qualified "
        "professional for consequential decisions."
    ),
    "zh": (
        "你是溫暖而有洞察力的紫微斗數與八字顧問。請在既有回答結構中，把技術資料編織成流暢、貼近個人的敘述，"
        "直接對使用者說明，所有細節都必須以實際命盤位置為根據。命盤資料是唯一可信的事實來源，不可捏造星曜位置或解讀。"
        "若使用者詢問你的名稱或角色，請自稱「命盤 · Destiny Chart 顧問」，並簡短說明你協助解讀命盤。"
        "不要主動提供後端資訊；若使用者直接詢問你是否為 AI，或詢問所使用的模型或服務提供者，請誠實簡短回答；"
        "只有在資訊確定時才說明模型或提供者，不可猜測，也不可自稱為人類。"
        "全程使用繁體中文，語言以目前介面設定為準，不受命盤或先前訊息語言影響。首次回答或新主題請使用三個標題："
        "「盤面解析」說明相關星曜、宮位及其原因；「行動指南」提供 2–3 項具體可執行建議；"
        "「延伸探索」提出相關追問。若使用者要求深入說明，直接提供專題解析與具體步驟，不重複標題或追問。"
        "語氣自然、具體，不作宿命論，描述趨勢而非定論。只使用提供的星曜定義與格局，說明其對此命盤的意義，"
        "不可自行添加格局。傳統命理解讀應表述為傳統觀點，不可當作科學事實；可說「傳統解讀可能將此格局與某種傾向相聯」。"
        "不必每次都附上網址；若使用者詢問來源，請說明來源背景與不確定性；即使未被詢問，對重要的不確定說法仍須加以限定。"
        "若問題同時涉及生活事件與內在心理，請自然融合紫微斗數的生活情境，以及八字傳統上對內在心理的詮釋；"
        "簡單或無關八字的問題，不要勉強加入八字。八字參考摘要僅供詮釋，不是額外命盤事實或科學性格評估。"
        "對需要深入解讀的問題，請在「行動指南」中以建議而非命令的口吻，提供實用且鼓舞人心的方向。"
        "涉及投資、醫療或法律時，提醒重大決策應諮詢合格專業人士。"
    ),
    "id": (
        "Anda adalah penasihat Zi Wei Dou Shu dan BaZi yang hangat dan berwawasan. Rangkai data teknis menjadi narasi "
        "personal yang mengalir dalam struktur jawaban yang sudah ada. Bicaralah langsung kepada pengguna dan dasarkan "
        "semua detail hanya pada posisi bagan yang benar-benar tersedia. Konteks bagan adalah satu-satunya sumber fakta bagan; "
        "Jika ditanya nama atau peran, perkenalkan diri sebagai Penasihat Destiny Chart yang membantu menafsirkan bagan. "
        "Jangan menyebut detail sistem di balik layanan secara proaktif. Jika ditanya langsung apakah Anda AI atau "
        "model/penyedia layanan yang digunakan, jawablah dengan jujur dan singkat; sebutkan model atau penyedia hanya "
        "jika informasinya diketahui, jangan menebak, dan jangan mengaku sebagai manusia. "
        "Jangan mengarang posisi atau tafsir. Jawab sepenuhnya dalam Bahasa Indonesia, terlepas "
        "dari bahasa konteks atau pesan sebelumnya. Untuk pertanyaan pertama atau topik baru, gunakan tiga bagian: "
        "Situasi (jelaskan faktor bagan yang relevan dan alasannya), Rencana Tindakan (berikan 2–3 langkah konkret "
        "yang dapat dilakukan), dan Pertanyaan Lanjutan (sarankan pertanyaan terkait). Jika pengguna meminta "
        "penjelasan lebih dalam, berikan analisis terarah dan langkah konkret tanpa mengulang bagian atau pertanyaan "
        "lanjutan. Gunakan nada alami, spesifik, dan tidak fatalistik; jelaskan kecenderungan, bukan kepastian. "
        "Gunakan hanya definisi bintang dan pola yang tersedia; jelaskan relevansinya bagi bagan pengguna dan jangan mengarang pola. "
        "Sajikan tafsir sebagai pandangan tradisional, bukan fakta ilmiah; misalnya, 'Tafsiran tradisional dapat mengaitkan pola ini dengan...'. "
        "Tidak perlu menyertakan URL di setiap jawaban. Jika pengguna meminta sumber, jelaskan asal-usul dan ketidakpastiannya; "
        "klaim yang secara material tidak pasti tetap harus diberi batasan meskipun tidak diminta. "
        "Jika pertanyaan menyangkut keadaan hidup sekaligus psikologi batin, padukan secara alami konteks kehidupan Zi Wei "
        "dengan tafsir tradisional BaZi tentang psikologi. Jangan memaksakan BaZi pada pertanyaan sederhana atau yang tidak terkait. "
        "Perlakukan ringkasan referensi BaZi sebagai panduan tafsir, bukan fakta bagan tambahan atau penilaian kepribadian ilmiah. "
        "Untuk pembacaan yang mendalam, akhiri bagian Rencana Tindakan dengan panduan yang praktis dan memberdayakan, sebagai saran bukan perintah. "
        "Untuk topik investasi, medis, atau hukum, ingatkan pengguna agar berkonsultasi dengan profesional berkualifikasi sebelum mengambil keputusan penting."
    ),
}

# Extra terminology rule (rule 7), written in the reply language.
TERM_RULES = {
    "en": (
        "7. Terminology: the chart data uses plain-English labels. Use only those exact labels. "
        "Never write Chinese characters and never write pinyin transliterations. "
        "Do not introduce concepts, stars or terms that are not in the chart data (for example qi or feng shui). "
        "When a label first appears, explain it in a few plain words."
    ),
    "id": (
        "7. Istilah: data bagan memakai label bahasa Indonesia yang sederhana. Gunakan hanya label persis tersebut. "
        "Jangan menulis karakter Mandarin dan jangan menulis transliterasi pinyin. "
        "Jangan menambahkan konsep, bintang, atau istilah yang tidak ada dalam data bagan (misalnya qi atau feng shui). "
        "Saat sebuah label pertama kali muncul, jelaskan dengan beberapa kata sederhana."
    ),
    "zh": "",
}

# Extra rule (rule 8), added only when a reference period is supplied.
PERIOD_RULES = {
    "en": (
        "8. The chart data ends with a reference date and the positions of the 10-year, yearly and monthly cycles. "
        "Answer for that period: begin by naming the period exactly as given in the reference date line, and never name any other date. "
        "The palace named for a cycle is the life area that cycle puts in focus. "
        "Do not make claims about any month or year that is not in the data. "
        "If earlier answers in this conversation covered a different period, do not reuse their time frame."
    ),
    "id": (
        "8. Data bagan diakhiri dengan tanggal acuan dan posisi siklus 10 tahun, tahunan, dan bulanan. "
        "Jawablah untuk periode itu: mulai dengan menyebut periode persis seperti pada baris tanggal acuan, dan jangan menyebut tanggal lain. "
        "Istana yang disebut untuk sebuah siklus adalah bidang kehidupan yang menjadi fokus siklus itu. "
        "Jangan membuat klaim tentang bulan atau tahun yang tidak ada dalam data. "
        "Jika jawaban sebelumnya dalam percakapan ini membahas periode lain, jangan gunakan kerangka waktunya."
    ),
    "zh": (
        "8. 命盤資料末尾附有運限參考日期，以及大限、流年、流月所落的宮位。"
        "請針對該時間段回答，開頭先照「運限參考日期」那一行說明時間段，不要提到其他日期。"
        "運限所落的宮位就是該時段的重點生活領域。資料中沒有的年份或月份，不要作任何斷言。"
        "若先前的回答針對的是其他時間段，請不要沿用該時間段。"
    ),
}

# Note attached to the user's latest question, so the period sits next to the question itself.
PERIOD_NOTE = {
    "en": "Answer for this period only: {line}. Ignore the time frame of earlier answers.",
    "id": "Jawab hanya untuk periode ini: {line}. Abaikan kerangka waktu jawaban sebelumnya.",
    "zh": "請只針對此時間段回答：{line}。請忽略先前回答的時間段。",
}

SYSTEM_PROMPT = "{language_instruction}\n\n{term_rules}\n\nChart context:\n{chart_context}"


def format_bazi(bazi_data):
    """Render a concise BaZi summary for the model context."""
    ten_gods = bazi_data["ten_gods"]
    stem_labels = (
        ("year_stem", "Year"),
        ("month_stem", "Month"),
        ("hour_stem", "Hour"),
    )
    gods = ", ".join(
        f"{label}: {ten_gods[key]}" for key, label in stem_labels
    )
    balance = ", ".join(
        f"{element} {count}"
        for element, count in bazi_data["elemental_balance"].items()
    )
    return (
        "\n\n【BaZi Four Pillars / 八字】\n"
        f"Day Master: {bazi_data['day_master']}\n"
        f"Ten Gods (Stems): {gods}\n"
        f"Elemental Balance: {balance}"
    )


def is_configured() -> bool:
    return OpenAI is not None and bool(_get_token())


def _get_token():
    # Streamlit secrets work locally and on Streamlit Community Cloud.
    try:
        import streamlit as st
        token = st.secrets.get("GROQ_API_KEY")
        if token and token != "your-key-here":
            return token
    except Exception:
        pass
    token = os.environ.get("GROQ_API_KEY")
    return token if token and token != "your-key-here" else None


def _client():
    token = _get_token()
    return OpenAI(base_url=GROQ_ENDPOINT, api_key=token)


def build_chart_context(bc, zw, interp_module) -> str:
    """Serialize the actual computed chart into plain text grounding
    context -- the same data the free/paid report already shows, just
    reformatted for the model instead of for display.
    (Built in Chinese; ask() translates it to the UI language.)"""
    pillars = bc.four_pillars.as_dict()
    lines = [
        f"四柱八字：{pillars['year']} {pillars['month']} {pillars['day']} {pillars['hour']}",
        f"日主：{pillars['day'][0]}",
        f"命主／身主：{zw.ming_zhu} / {zw.shen_zhu}",
        f"五行局：{zw.bureau_name}",
        "",
        "十二宮：",
    ]
    for row in zw.palace_table():
        stars = "、".join(row["stars"]) or "無主星"
        body_tag = "（身宮）" if row["is_body_palace"] else ""
        d_start, d_end = row["decade"]["range"]
        lines.append(f"- {row['palace']}{body_tag}：{row['stem']}{row['branch']}，主星：{stars}，大限：{d_start}-{d_end}歲")
    return "\n".join(lines)


def _clean_reply(text: str, lang: str) -> str:
    """For en/id: translate any Chinese terms the model still wrote, then remove
    leftover Chinese characters. Chinese replies are returned unchanged."""
    if lang == "zh" or not text:
        return text
    text = translate_text(text, lang)
    if leftover_chinese(text):
        log.warning("ai_chat: removing leftover Chinese from reply: %s",
                    "".join(sorted(leftover_chinese(text))))
        # drop parentheses that only held Chinese, then any remaining Chinese characters
        text = re.sub(r"\s*[（(][^()（）]*[\u4e00-\u9fff][^()（）]*[)）]", "", text)
        text = re.sub(r"[\u4e00-\u9fff]+", "", text)
        text = re.sub(r" {2,}", " ", text)
    pin = find_pinyin(text)
    if pin:
        log.warning("ai_chat: pinyin found in reply: %s", pin)
    return text.strip()


def ask(chart_context: str, chat_history: list, user_question: str, ui_lang: str = "zh",
        period_context=None, star_definitions=None, patterns=None,
        bazi_context=None, bazi_reference=None) -> str:
    """chat_history: list of {'role': 'user'|'assistant', 'content': str}
    period_context: text from period_engine (already in the UI language). If None, it is
    read from st.session_state["period_ctx"], which the period selector fills in."""
    if not is_configured():
        raise RuntimeError("Groq not configured (missing GROQ_API_KEY or openai package).")

    lang = ui_lang if ui_lang in LANGUAGE_INSTRUCTIONS else "zh"

    client = _client()
    language_instruction = LANGUAGE_INSTRUCTIONS[lang]
    # Translate the chart facts by meaning so the model never sees Chinese terms
    # (and therefore never copies or romanizes them) in en / id mode.
    chart_context = translate_text(chart_context, lang)
    if star_definitions:
        from knowledge_lookup import format_star_definitions
        chart_context = chart_context + format_star_definitions(star_definitions, lang)
    if patterns:
        from knowledge_lookup import format_patterns
        chart_context = chart_context + format_patterns(patterns, lang)
    if bazi_context:
        chart_context = chart_context + format_bazi(bazi_context)
    if bazi_reference:
        chart_context = (
            chart_context
            + "\n\n【BaZi Reference / 八字解讀】\n"
            + bazi_reference
        )
    period_header = ""
    if period_context is None:
        try:
            import streamlit as st
            period_context = st.session_state.get("period_ctx", "")
            period_header = st.session_state.get("period_header", "")
        except Exception:
            period_context = ""
    term_rules = TERM_RULES[lang]
    if period_context:
        chart_context = chart_context + "\n\n" + period_context
        term_rules = (term_rules + "\n" + PERIOD_RULES[lang]).strip()
    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT.format(
            chart_context=chart_context,
            language_instruction=language_instruction,
            term_rules=term_rules,
        ),
    }]
    sanitized_history = [
        {"role": message["role"], "content": message["content"]}
        for message in chat_history
    ]
    messages.extend(sanitized_history)
    final_question = user_question
    if period_context:
        first_line = period_context.split("\n")[0]
        final_question = user_question + "\n\n(" + PERIOD_NOTE[lang].format(line=first_line) + ")"
    messages.append({"role": "user", "content": final_question})

    stream = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
        stream=True,
    )
    if period_header:
        # Code-written label: shows the user exactly which period this answer used.
        yield "*" + period_header + "*\n\n"
    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
