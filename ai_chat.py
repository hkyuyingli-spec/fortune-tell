"""
Conversational Q&A about a computed chart, backed by Groq.

Design principle: the model is NOT asked to invent or extend the chart.
It is given the exact computed facts (four pillars, palaces, stars,
bureau, decades) as grounding context and instructed to answer only from
those facts, in the same reflective/non-deterministic register as the
rest of this app's interpretation text.
"""
import os

try:
    from groq import Groq
    from groq import APIConnectionError, APIError, APIStatusError, RateLimitError
except ImportError:  # pragma: no cover
    Groq = None
    APIConnectionError = APIError = APIStatusError = RateLimitError = Exception

DEFAULT_MODEL = "openai/gpt-oss-20b"
AVAILABLE_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-safeguard-20b",
]

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
    return Groq is not None and bool(_get_token())


def _get_token() -> str | None:
    """Get the Groq API key from Streamlit secrets first, then env as fallback."""
    try:
        import streamlit as st
        value = st.secrets.get("GROQ_API_KEY")
        if value:
            return str(value)
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY")


def _client() -> Groq:
    token = _get_token()
    if not token:
        raise RuntimeError("Groq API key missing. Add GROQ_API_KEY in Streamlit secrets or environment.")
    return Groq(api_key=token)


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


def _resolve_model(model_name: str | None) -> str:
    model = (model_name or DEFAULT_MODEL).strip()
    return model if model in AVAILABLE_MODELS else DEFAULT_MODEL


def ask(chart_context: str, chat_history: list, user_question: str, model: str = DEFAULT_MODEL, stream: bool = False):
    """chat_history: list of {'role': 'user'|'assistant', 'content': str}

    Returns a plain string by default; when stream=True, it streams chunks and
    concatenates them into one final string so the existing app interface stays unchanged.
    """
    if not is_configured():
        raise RuntimeError("Groq not configured (missing GROQ_API_KEY or groq package).")

    resolved_model = _resolve_model(model)

    client = _client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(chart_context=chart_context)}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_question})

    try:
        response = client.chat.completions.create(
            model=resolved_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=stream,
        )

        if stream:
            chunks = []
            for chunk in response:
                delta = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta else ""
                if delta:
                    chunks.append(delta)
            return "".join(chunks)

        content = response.choices[0].message.content
        return content or ""
    except RateLimitError as exc:
        raise RuntimeError(f"Groq rate limit exceeded. Please try again in a moment. ({exc})") from exc
    except APIConnectionError as exc:
        raise RuntimeError(f"Groq network error: could not connect to the Groq API. ({exc})") from exc
    except (APIStatusError, APIError, TimeoutError) as exc:
        raise RuntimeError(f"Groq API error: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Unable to generate Groq response: {exc}") from exc
