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

SYSTEM_PROMPT = """Σ╜áµÿ»πÇîσæ╜τ¢ñ ┬╖ Destiny ChartπÇìτÜäσæ╜τ¢ñσòÅτ¡öσè⌐µëïπÇéΣ╜┐τö¿ΦÇàσ╖▓τ╢ôτ«ùσç║Φç¬σ╖▒τÜäτ┤½σ╛«µûùµò╕∩╝Åσà½σ¡ùσæ╜τ¢ñ∩╝î
Σ╗ÑΣ╕ïµÿ»ΘÇÖσ╝╡σæ╜τ¢ñτÜäσ«îµò┤Φ¿êτ«ùτ╡Éµ₧£∩╝êΘÇÖµÿ»σö»Σ╕ÇσÅ»Σ┐íτÜäΣ║ïσ»ªΣ╛åµ║É∩╝îΣ╕ìσÅ»Φç¬Φíîµ¢┤µö╣µêûσ╗╢Σ╝╕∩╝ë∩╝Ü

{chart_context}

σ¢₧τ¡öΦªÅσëç∩╝êσïÖσ┐àΘü╡σ«ê∩╝ë∩╝Ü
1. σÅ¬µá╣µôÜΣ╕èΘ¥óµÅÉΣ╛¢τÜäσæ╜τ¢ñΣ║ïσ»ªσ¢₧τ¡ö∩╝îΣ╕ìσÅ»µìÅΘÇáΣ╕èΘ¥óµ▓Æµ£ëτÜäµÿƒµ¢£πÇüσ««Σ╜ìµêûσñºΘÖÉΦ│çΦ¿èπÇé
2. Φ¬₧µ░úτ╢¡µîüπÇîσÅìµÇ¥∩╝ÅµÄóτ┤óπÇì∩╝îΣ╕ìΦªüτ╡ªσç║τ╡òσ░ìπÇüσ«┐σæ╜σ╝ÅτÜäµû╖Φ¿Ç∩╝êΣ╛ïσªéπÇîΣ╜áΣ╕Çσ«Üµ£â...πÇì∩╝ë∩╝î
   σñÜτö¿πÇîΘÇÖσÇïτ╡äσÉêσé│τ╡▒Σ╕èΣ╗úΦí¿...πÇìπÇîσÅ»Σ╗Ñµâ│µâ│...πÇìΘÇÖΘí₧Φí¿Φ┐░πÇé
3. Σ╕ìσ░ìΘå½τÖéπÇüµ│òσ╛ïπÇüµèòΦ│çτ¡ëΘçìσñºΣ║║τöƒµ▒║τ¡ûτ╡ªσç║σà╖Θ½öσ╗║Φ¡░∩╝¢σªéµ₧£Σ╜┐τö¿ΦÇàσòÅΘÇÖΘí₧σòÅΘíî∩╝î
   σ╝òσ░ÄΣ╗ûσÇæµèèσæ╜τ¢ñτò╢Σ╜£σÅìµÇ¥τÜäΦ╡╖Θ╗₧∩╝îΣ╕ªσ╗║Φ¡░Φ½«Φ⌐óσ░êµÑ¡Σ║║σú½πÇé
4. σªéµ₧£Σ╜┐τö¿ΦÇàτÜäσòÅΘíîΦ╢àσç║ΘÇÖσ╝╡σæ╜τ¢ñΦâ╜σ¢₧τ¡öτÜäτ»äσ£ì∩╝êΣ╛ïσªéσòÅσê░Θéäµ▓Æσ»ªΣ╜£τÜäΦ╝öµÿƒπÇüσ¢¢σîûπÇü
   ΘÇÉµ£êµ╡üµ¢£∩╝ë∩╝îΦ¬áσ»ªΦ¬¬µÿÄτ¢«σëìτ│╗τ╡▒Θéäµ▓Æµ£ëΘÇÖΘâ¿σêåΦ│çµûÖ∩╝îΣ╕ìΦªüτ╖¿ΘÇáπÇé
5. τö¿Σ╜┐τö¿ΦÇàµÅÉσòÅτÜäΦ¬₧Φ¿Çσ¢₧Φªå∩╝êΣ╕¡µûçµÅÉσòÅτö¿Σ╕¡µûç∩╝îΦï▒µûçµÅÉσòÅτö¿Φï▒µûç∩╝ëπÇé
6. σ¢₧τ¡öΣ┐¥µîüτ░íµ╜ö∩╝îΣ╕ÇΦê¼ 2-4 σÅÑΦ⌐▒∩╝îΘÖñΘ¥₧Σ╜┐τö¿ΦÇàΦªüµ▒éµ¢┤Φ⌐│τ┤░τÜäΦ¬¬µÿÄπÇé
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
        f"σ¢¢µƒ▒σà½σ¡ù∩╝Ü{pillars['year']} {pillars['month']} {pillars['day']} {pillars['hour']}",
        f"µùÑΣ╕╗∩╝Ü{pillars['day'][0]}",
        f"σæ╜Σ╕╗∩╝ÅΦ║½Σ╕╗∩╝Ü{zw.ming_zhu} / {zw.shen_zhu}",
        f"Σ║öΦíîσ▒Ç∩╝Ü{zw.bureau_name}",
        "",
        "σìüΣ║îσ««∩╝Ü",
    ]
    for row in zw.palace_table():
        stars = "πÇü".join(row["stars"]) or "τäíΣ╕╗µÿƒ"
        body_tag = "∩╝êΦ║½σ««∩╝ë" if row["is_body_palace"] else ""
        d_start, d_end = row["decade"]["range"]
        lines.append(f"- {row['palace']}{body_tag}∩╝Ü{row['stem']}{row['branch']}∩╝îΣ╕╗µÿƒ∩╝Ü{stars}∩╝îσñºΘÖÉ∩╝Ü{d_start}-{d_end}µ¡▓")
    return "\n".join(lines)


def _extract_completion_text(response) -> str:
    """Support the normal OpenAI object shape and fail with a clear message if
    the provider returns an unexpected payload type."""
    if hasattr(response, "choices"):
        choices = getattr(response, "choices")
        if choices and hasattr(choices[0], "message"):
            message = getattr(choices[0], "message")
            if hasattr(message, "content"):
                return message.content
            if isinstance(message, dict) and "content" in message:
                return message["content"]

    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices:
            first = choices[0]
            message = first.get("message") if isinstance(first, dict) else None
            if isinstance(message, dict) and "content" in message:
                return message["content"]

    if isinstance(response, str):
        raise RuntimeError("GitHub Models returned a plain string instead of a chat completion object.")

    raise RuntimeError(f"Unexpected GitHub Models response type: {type(response).__name__}")


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
    return _extract_completion_text(response)
