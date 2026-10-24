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
DEFAULT_MODEL = "openai/gpt-oss-20b"

LANGUAGE_INSTRUCTIONS = {
    "en": "Reply entirely in English. This selected UI language takes precedence over the language used in the chart context and prior messages.",
    "zh": "請全程使用繁體中文（繁體中文）回答。此 UI 語言優先於命盤內容與先前訊息使用的語言。",
    "id": "Jawab sepenuhnya dalam Bahasa Indonesia. Bahasa UI yang dipilih ini lebih diutamakan daripada bahasa dalam konteks bagan dan pesan sebelumnya.",
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

SYSTEM_PROMPT = """你是「命盤 · Destiny Chart」的專業紫微斗數顧問。使用者已經算出命盤，以下是這張命盤的完整資料（這是唯一可信的事實來源，不可捏造）：

{chart_context}

【你的回答結構（每次回答都必須包含這三部分）】：
1. 盤面解析 (The Situation)：根據用戶的提問（如財富、事業、感情），結合提供的星曜與宮位，用白話文解釋目前的能量狀態。
2. 行動指南 (The Action Plan)：這是最重要的部分！不要只說「你會怎樣」，請給出 2-3 個具體、可執行的建議。例如：「這個月適合整理財務」、「建議避開合約簽署」、「可以多參與社交活動」。如果涉及投資/醫療/法律，請加上「命理僅供參考，重大決策請諮詢專業人士」。
3. 延伸探索 (The Hook)：根據目前的盤面，引導用戶詢問下一個相關的問題（例如：「既然你問了不動產，你想順便看看你目前的現金流（財帛宮）嗎？」）。

【語氣與規則】：
- 不要給出絕對宿命論（如「你一定會發財」），但要給出明確的趨勢與行動建議。
- 如果用戶問得很簡短（如「advise for this month」），請主動根據流月/流年宮位，給出這個月的具體運勢與行動指南。
- {language_instruction}
- 回答長度約 150-300 字，確保細節充足，絕不敷衍。
{term_rules}
"""


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
        period_context=None) -> str:
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
    messages.extend(chat_history)
    final_question = user_question
    if period_context:
        first_line = period_context.split("\n")[0]
        final_question = user_question + "\n\n(" + PERIOD_NOTE[lang].format(line=first_line) + ")"
    messages.append({"role": "user", "content": final_question})

    raw = client.chat.completions.with_raw_response.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1200,
    )
    http_resp = raw.http_response
    if http_resp.headers.get("content-type", "").startswith("text/plain"):
        raise RuntimeError(
            f"Non-JSON reply -- status={http_resp.status_code}, "
            f"content-type={http_resp.headers.get('content-type')}, "
            f"url={http_resp.request.url}, body={http_resp.text[:200]}"
        )
    response = raw.parse()
    if isinstance(response, str):
        snippet = response.strip()[:300]
        raise RuntimeError(
            "Groq replied with plain text instead of a chat completion: "
            f"{snippet!r}. Check GROQ_API_KEY and Groq API access."
        )
    reply = _clean_reply(response.choices[0].message.content, lang)
    if period_header:
        # Code-written label: shows the user exactly which period this answer used.
        reply = "*" + period_header + "*\n\n" + reply
    return reply
