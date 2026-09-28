"""
Conversational Q&A about a computed chart, backed by GitHub Models
(https://github.blog/ai-and-ml/llms/solving-the-inference-problem-for-open-source-ai-projects-with-github-models/) --
a free, OpenAI-compatible inference API authenticated with a GitHub
Personal Access Token, rather than a separate paid AI vendor key.

Design principle: the model is NOT asked to invent or extend the chart.
It is given the exact computed facts (four pillars, palaces, stars,
bureau, decades) as grounding context and instructed to answer only from
those facts, in the same reflective/non-deterministic register as the
rest of this app's interpretation text. This keeps the chat feature
consistent with the app's own disclaimer instead of letting a general-
purpose LLM freelance new "predictions" the engine never computed.
"""
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-4o-mini"

SYSTEM_PROMPT = """你是「命盤 · Destiny Chart」的命盤問答助手。使用者已經算出自己的紫微斗數／八字命盤，
以下是這張命盤的完整計算結果（這是唯一可信的事實來源，不可自行更改或延伸）：

{chart_context}

回答規則（務必遵守）：
1. 只根據上面提供的命盤事實回答，不可捏造上面沒有的星曜、宮位或大限資訊。
2. 語氣維持「反思／探索」，不要給出絕對、宿命式的斷言（例如「你一定會...」），
   多用「這個組合傳統上代表...」「可以想想...」這類表述。
3. 不對醫療、法律、投資等重大人生決策給出具體建議；如果使用者問這類問題，
   引導他們把命盤當作反思的起點，並建議諮詢專業人士。
4. 如果使用者的問題超出這張命盤能回答的範圍（例如問到還沒實作的輔星、四化、
   逐月流曜），誠實說明目前系統還沒有這部分資料，不要編造。
5. 用使用者提問的語言回覆（中文提問用中文，英文提問用英文）。
6. 回答保持簡潔，一般 2-4 句話，除非使用者要求更詳細的說明。
"""


def is_configured() -> bool:
    return OpenAI is not None and bool(_get_token())


def _get_token():
    # Prefer Streamlit secrets when running under Streamlit; fall back to
    # a plain environment variable for local/non-Streamlit use.
    try:
        import streamlit as st
        if "GITHUB_TOKEN" in st.secrets:
            return st.secrets["GITHUB_TOKEN"]
    except Exception:
        pass
    return os.environ.get("GITHUB_TOKEN")


def _client():
    token = _get_token()
    return OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=token)


def build_chart_context(bc, zw, interp_module) -> str:
    """Serialize the actual computed chart into plain text grounding
    context -- the same data the free/paid report already shows, just
    reformatted for the model instead of for display."""
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


def ask(chart_context: str, chat_history: list, user_question: str) -> str:
    """chat_history: list of {'role': 'user'|'assistant', 'content': str}"""
    if not is_configured():
        raise RuntimeError("GitHub Models not configured (missing GITHUB_TOKEN or openai package).")

    client = _client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(chart_context=chart_context)}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )
    if isinstance(response, str):
        raise RuntimeError("GitHub Models replied with plain text: " + response[:300])
    return response.choices[0].message.content
