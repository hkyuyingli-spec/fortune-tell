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

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
except ImportError:  # pragma: no cover
    TfidfVectorizer = None
    LogisticRegression = None
    make_pipeline = None

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

QUESTION_CATEGORIES = ["wealth", "career", "love", "property", "business", "general"]

QUESTION_TRAINING_DATA = {
    "wealth": [
        "財運", "投資", "理財", "賺錢", "財務", "金錢", "收入", "財富", "理財建議", "投資機會",
        "賺錢方向", "存款", "錢", "投資方向", "財產", "财富", "收益", "賺錢", "財運好不好"
    ],
    "career": [
        "職涯", "工作", "工作發展", "職場", "事業", "升遷", "升職", "職業", "工作前途", "職涯方向",
        "事業方向", "職場發展", "工作運勢", "找工作", "事業發展", "工作會順嗎", "我的工作"
    ],
    "love": [
        "戀愛", "感情", "另一半", "婚姻", "桃花", "伴侶", "戀愛運", "感情問題", "感情模式", "婚姻運",
        "緣分", "伴侶關係", "戀愛前景", "感情發展", "相處模式", "感情穩定", "婚姻關係"
    ],
    "property": [
        "房產", "購屋", "房地產", "房貸", "買房", "居住", "家宅", "置產", "房子", "物業", "住家", "住宅"
    ],
    "business": [
        "創業", "做生意", "商業", "經營", "事業", "企業", "商機", "合作", "市場", "加盟", "生意", "業務", "商業前景"
    ],
    "general": [
        "命盤", "性格", "命運", "人生", "個性", "整體", "人生方向", "命理", "運勢", "大致看法"
    ],
}


def _fallback_classify_question(question: str):
    text = (question or "").lower()
    if not text.strip():
        return "general", 0.5

    scores = {}
    for label, keywords in QUESTION_TRAINING_DATA.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        scores[label] = score

    best_label, best_score = max(scores.items(), key=lambda item: item[1])
    if best_score == 0:
        return "general", 0.5

    confidence = min(0.99, 0.55 + (best_score / max(1, len(QUESTION_TRAINING_DATA[best_label])) * 0.45))
    return best_label, round(confidence, 3)


def _build_question_model():
    if TfidfVectorizer is None or make_pipeline is None or LogisticRegression is None:
        return None

    samples = []
    labels = []
    for label, phrases in QUESTION_TRAINING_DATA.items():
        for phrase in phrases:
            samples.append(phrase)
            labels.append(label)

    model = make_pipeline(
        TfidfVectorizer(analyzer="char", ngram_range=(2, 4), lowercase=False),
        LogisticRegression(max_iter=2000, random_state=42),
    )
    model.fit(samples, labels)
    return model


QUESTION_MODEL = _build_question_model()


def classify_question(question: str):
    """Classify a user question into a chart-related intent category.

    Hybrid approach: keyword scores provide strong signal for common expressions,
    then a lightweight trained ML model is used as a fallback for future unseen
    questions. Returns (label, confidence).
    """
    text = (question or "").strip()
    if not text:
        return "general", 0.5

    lower_text = text.lower()
    keyword_scores = {}
    for label, phrases in QUESTION_TRAINING_DATA.items():
        score = 0
        for phrase in phrases:
            phrase_lower = phrase.lower()
            if phrase_lower in lower_text:
                score += 2
            elif phrase_lower in {"工作", "財運", "戀愛", "感情", "房產", "創業", "命盤"}:
                if phrase_lower in lower_text:
                    score += 1
            elif any(token in lower_text for token in phrase_lower):
                score += 1
        keyword_scores[label] = score

    best_keyword_label, best_keyword_score = max(keyword_scores.items(), key=lambda item: item[1])
    if best_keyword_score > 0:
        base_confidence = 0.55 + (best_keyword_score / max(1, len(QUESTION_TRAINING_DATA[best_keyword_label])) * 0.45)
        return best_keyword_label, round(min(0.99, base_confidence), 3)

    if QUESTION_MODEL is not None:
        prediction = QUESTION_MODEL.predict([text])[0]
        probabilities = QUESTION_MODEL.predict_proba([text])[0]
        idx = list(QUESTION_MODEL.classes_).index(prediction)
        confidence = float(probabilities[idx])
        return prediction, round(confidence, 3)

    return _fallback_classify_question(text)


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


def build_profile_context(profile: dict | None) -> str:
    """Serialize a small user intent profile into a prompt hint."""
    if not isinstance(profile, dict) or not profile:
        return ""
    ordered = sorted(profile.items(), key=lambda item: item[1], reverse=True)
    parts = [f"{label}={count}" for label, count in ordered[:5]]
    return ", ".join(parts) if parts else ""


def sanitize_chat_history(chat_history: list | None) -> list:
    """Normalize chat history so it is always a list of dicts with role/content."""
    if not isinstance(chat_history, list):
        return []

    cleaned = []
    for item in chat_history:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant", "system"}:
            continue
        if content is None:
            continue
        cleaned.append({"role": role, "content": str(content)})
    return cleaned


def ask(chart_context: str, chat_history: list, user_question: str, model: str = DEFAULT_MODEL, stream: bool = False, profile_context: dict | None = None):
    """chat_history: list of {'role': 'user'|'assistant', 'content': str}

    Returns a plain string by default; when stream=True, it streams chunks and
    concatenates them into one final string so the existing app interface stays unchanged.
    """
    if not is_configured():
        raise RuntimeError("Groq not configured (missing GROQ_API_KEY or groq package).")

    sanitized_history = sanitize_chat_history(chat_history)
    resolved_model = _resolve_model(model)
    intent_label, intent_confidence = classify_question(user_question)
    profile_hint = build_profile_context(profile_context)

    client = _client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(chart_context=chart_context)}]
    messages.append({
        "role": "system",
        "content": f"User intent classification: {intent_label} (confidence={intent_confidence:.3f}). Focus on this question category while preserving chart-only grounding.",
    })
    if profile_hint:
        messages.append({
            "role": "system",
            "content": f"User personalization profile: {profile_hint}. Use this to prioritize recent question themes, but still answer only from the chart facts and never invent data.",
        })
    messages.extend(sanitized_history)
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
