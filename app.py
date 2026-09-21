import re
import datetime
import streamlit as st

from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart
import interpretation as interp
import rectification as rect
import ai_chat
import firebase_db
from i18n import t, LANGS

st.set_page_config(page_title="Destiny Chart", page_icon="🔮", layout="centered")

st.markdown("""
<style>
:root {
    --ink:#14182A; --paper:#EFE7D8; --cinnabar:#B23A2E; --gold:#C9A15A; --jade:#4B7A6D; --charcoal:#23262F;
}
.stApp { background: var(--ink); }
h1 { font-family: "Noto Serif TC", serif !important; color: var(--gold) !important; }
h2, h3 { color: var(--gold) !important; font-family: "Noto Serif TC", serif !important; }

/* Page-level text (labels, captions, radio options) sits directly on the
   dark ink background, so it needs to be light -- Streamlit's default
   text color here is a muted gray meant for light backgrounds and is
   very low-contrast against navy. */
.stMarkdown, .stMarkdown p, .stCaption, label, .stRadio div[role="radiogroup"] label p {
    color: var(--paper) !important;
}

/* Cards (free/paid tier, info banner) sit on a light paper background,
   so THEIR text needs to be dark -- these selectors are more specific
   than the rule above, so they correctly win. */
.free-card, .paid-card, .info-card {
    background: var(--paper); border-radius: 6px;
    padding: 24px 28px; margin-bottom: 18px;
}
.free-card h3, .paid-card h3 { color: var(--cinnabar) !important; font-family: "Noto Serif TC", serif !important; margin-top: 0; }
.free-card p, .paid-card p, .info-card, .palace-row, .palace-row b, .decade-tag {
    color: var(--charcoal) !important;
}
.paid-card { border-left: 4px solid var(--cinnabar); }
.info-card { border: 1px dashed var(--jade); font-size: 14px; }
.palace-row { border-bottom: 1px dotted rgba(35,38,47,0.25); padding: 10px 0; }
.decade-tag { color: #8a7b6c !important; }
.disclaimer { color: var(--gold) !important; font-size: 12.5px; margin-top: 18px; line-height:1.6; }
.candidate-box { background: var(--paper); border: 1px solid rgba(35,38,47,0.2); border-radius: 4px; padding: 10px 14px; margin-bottom: 8px; color: var(--charcoal) !important; }
.rect-card { background: var(--paper); color: var(--charcoal) !important; border-left: 4px solid var(--jade); border-radius: 6px; padding: 24px 28px; margin-bottom: 18px; }
.block-container { max-width: 720px; }
</style>
""", unsafe_allow_html=True)

# ---- language selector (top of page, controls everything below) ----
lang_codes = list(LANGS.keys())
lang = st.selectbox(
    t("language_label", "zh"),
    lang_codes,
    format_func=lambda code: LANGS[code],
    index=0,
    key="lang_select",
)

st.title(t("app_title", lang))
st.caption(t("app_caption", lang))


def _md_to_html(text: str) -> str:
    """Tiny markdown->HTML helper so we can build ONE self-contained HTML
    block per call. Streamlit renders each separate st.markdown()/
    st.subheader() call as its own independent DOM node -- opening a
    <div> in one call and closing it in another does NOT actually nest
    the content in between, it leaves an empty styled box and dumps the
    real content outside it with default (unreadable-on-dark) styling.
    Building one full HTML string per visual "card" avoids that."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(f"<p>{p}</p>" for p in paras)


def render_full_report(bc: BirthChart, zw: ZiWeiChart, lang: str):
    """Shared rendering for a resolved chart (whether time was known
    upfront, or arrived at via 定盤 rectification)."""
    pillars = bc.four_pillars.as_dict()

    # Log once per distinct chart, not on every widget-triggered rerun
    # (Streamlit reruns the whole script on every interaction, so without
    # this guard the same chart would get logged dozens of times).
    log_key = f"{bc.solar_year}-{bc.solar_month}-{bc.solar_day}-{bc.hour}-{zw.gender}"
    if st.session_state.get("logged_chart_key") != log_key:
        st.session_state["logged_chart_key"] = log_key
        life_row = zw.palace_table()[0]
        firebase_db.log_chart_request({
            "lang": lang,
            "mode": st.session_state.get("mode"),
            "gender": zw.gender,
            "birth_year": bc.solar_year,
            "birth_month": bc.solar_month,
            "day_master": pillars["day"][0],
            "bureau_name": zw.bureau_name,
            "life_palace_stars": life_row["stars"],
        })

    free_html = _md_to_html(interp.free_tier_summary(pillars, pillars["day"][0], zw, lang))
    st.markdown(f'<div class="free-card"><h3>{t("free_tier_header", lang)}</h3>{free_html}</div>', unsafe_allow_html=True)

    if not st.session_state.get("unlocked"):
        st.markdown(f'<div class="info-card">{t("unlock_info", lang)}</div>', unsafe_allow_html=True)
        if st.button(t("unlock_btn", lang)):
            st.session_state["unlocked"] = True
            st.rerun()
    else:
        current_year = datetime.date.today().year
        rows, current_palace = interp.paid_tier_report(zw, current_year, lang)

        parts = ['<div class="paid-card">', f"<h3>{t('paid_tier_header', lang)}</h3>"]
        if current_palace:
            parts.append(f"<p><b>{current_year}{t('current_year_palace', lang)}{current_palace}</b></p>")
        for row in rows:
            parts.append(
                f"""<div class="palace-row">
                <b>{row['palace']}</b>（{row['meaning']}）— {row['stem_branch']}<br/>
                {row['stars']}<br/>
                {row['blurb']}<br/>
                <span class="decade-tag">{t('decade_label', lang)}{row['decade_range']}</span>
                </div>"""
            )
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

    st.markdown(f'<p class="disclaimer">{t("disclaimer", lang)}</p>', unsafe_allow_html=True)
    if firebase_db.is_configured():
        st.markdown(f'<p class="disclaimer">{t("privacy_note", lang)}</p>', unsafe_allow_html=True)

    if st.session_state.get("unlocked"):
        render_ai_chat(bc, zw, lang)


CATEGORIES = [
    ("cat_wealth", "cat_q_wealth"),
    ("cat_career", "cat_q_career"),
    ("cat_love", "cat_q_love"),
    ("cat_property", "cat_q_property"),
    ("cat_business", "cat_q_business"),
]


def _send_question(bc, zw, lang, question, category=None):
    st.session_state["chat_history"].append({"role": "user", "content": question})
    try:
        context = ai_chat.build_chart_context(bc, zw, interp)
        answer = ai_chat.ask(context, st.session_state["chat_history"][:-1], question)
    except Exception as e:
        answer = f"Error: {e}"
    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
    firebase_db.log_chat_message({
        "lang": lang,
        "chart_key": st.session_state.get("chat_chart_key"),
        "category": category,
        "question": question,
        "answer": answer,
    })


def render_ai_chat(bc: BirthChart, zw: ZiWeiChart, lang: str):
    st.markdown(f"### {t('ai_chat_header', lang)}")

    if not ai_chat.is_configured():
        st.warning(t("ai_not_configured", lang))
        return

    chart_key = f"{bc.solar_year}-{bc.solar_month}-{bc.solar_day}-{bc.hour}"
    if st.session_state.get("chat_chart_key") != chart_key:
        st.session_state["chat_chart_key"] = chart_key
        st.session_state["chat_history"] = []

    st.caption(t("ai_category_header", lang))
    cols = st.columns(len(CATEGORIES))
    for col, (label_key, question_key) in zip(cols, CATEGORIES):
        with col:
            if st.button(t(label_key, lang), key=f"cat_{label_key}", use_container_width=True):
                with st.spinner(t("ai_thinking", lang)):
                    _send_question(bc, zw, lang, t(question_key, lang), category=label_key)
                st.rerun()

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(t("ai_chat_placeholder", lang))
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner(t("ai_thinking", lang)):
                context = ai_chat.build_chart_context(bc, zw, interp)
                try:
                    answer = ai_chat.ask(context, st.session_state["chat_history"], question)
                except Exception as e:
                    answer = f"Error: {e}"
                st.write(answer)
        st.session_state["chat_history"].append({"role": "user", "content": question})
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        firebase_db.log_chat_message({
            "lang": lang,
            "chart_key": st.session_state.get("chat_chart_key"),
            "category": "free_text",
            "question": question,
            "answer": answer,
        })


mode = st.radio(
    t("know_time_q", lang),
    ["know_time", "unknown_time"],
    format_func=lambda m: t("know_time_yes", lang) if m == "know_time" else t("know_time_no", lang),
    horizontal=False,
)

# Reset the flow's state if the mode changes
if st.session_state.get("mode") != mode:
    st.session_state["mode"] = mode
    st.session_state.pop("chart_input", None)
    st.session_state.pop("rect_step", None)
    st.session_state.pop("rect_candidates", None)
    st.session_state.pop("rect_candidates_narrowed", None)
    st.session_state.pop("rect_final", None)
    st.session_state.pop("chat_history", None)
    st.session_state.pop("chat_chart_key", None)
    st.session_state["unlocked"] = False

# ============================== KNOW TIME ==============================
if mode == "know_time":
    with st.form("birth_form"):
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input(t("birth_date", lang), value=datetime.date(1990, 1, 1),
                                        min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
        with col2:
            birth_time = st.time_input(t("birth_time", lang), value=datetime.time(12, 0))
        gender = st.radio(t("gender", lang), ["male", "female"],
                           format_func=lambda g: t("male", lang) if g == "male" else t("female", lang), horizontal=True)
        submitted = st.form_submit_button(t("reveal_btn", lang))

    if submitted:
        st.session_state["chart_input"] = (birth_date, birth_time, gender)
        st.session_state["unlocked"] = False

    if "chart_input" in st.session_state:
        birth_date, birth_time, gender = st.session_state["chart_input"]
        bc = BirthChart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
        zw = ZiWeiChart(bc, gender)
        render_full_report(bc, zw, lang)

# ============================== UNKNOWN TIME: 定盤 ==============================
else:
    st.markdown(f'<div class="rect-card">{t("rect_intro", lang)}</div>', unsafe_allow_html=True)

    step = st.session_state.get("rect_step", "input")

    if step == "input":
        with st.form("rect_form"):
            col1, col2 = st.columns(2)
            with col1:
                r_date = st.date_input(t("birth_date", lang), value=datetime.date(1990, 1, 1),
                                        min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
            with col2:
                r_gender = st.radio(t("gender", lang), ["male", "female"],
                                     format_func=lambda g: t("male", lang) if g == "male" else t("female", lang), horizontal=True)
            go = st.form_submit_button(t("rect_start_btn", lang))
        if go:
            candidates = rect.generate_candidates(r_date.year, r_date.month, r_date.day, r_gender)
            st.session_state["rect_candidates"] = candidates
            st.session_state["rect_step"] = "personality"
            st.rerun()

    elif step == "personality":
        candidates = st.session_state["rect_candidates"]
        pq = rect.personality_question(candidates, lang)
        st.subheader(t("rect_step1_header", lang))
        options = [text for text, _ in pq]
        choice = st.radio(t("rect_step1_caption", lang), options, index=None)
        if choice is not None and st.button(t("rect_next_btn", lang)):
            chosen_idxs = dict(pq)[choice]
            narrowed = rect.narrow_by_personality(candidates, chosen_idxs)
            st.session_state["rect_candidates_narrowed"] = narrowed
            st.session_state["rect_step"] = "turning_point"
            st.rerun()

    elif step == "turning_point":
        narrowed = st.session_state["rect_candidates_narrowed"]
        st.subheader(t("rect_step2_header", lang))
        st.caption(t("rect_step2_caption", lang))
        age = st.slider(t("rect_age_label", lang), 5, 60, 25)
        col1, col2 = st.columns(2)
        with col1:
            confirm = st.button(t("rect_confirm_age_btn", lang))
        with col2:
            skip = st.button(t("rect_skip_btn", lang))
        if confirm:
            narrowed2, did_narrow = rect.narrow_by_turning_point(narrowed, age)
            if not did_narrow:
                st.session_state["rect_turning_point_note"] = t("rect_no_narrow_note", lang)
            else:
                st.session_state.pop("rect_turning_point_note", None)
            st.session_state["rect_candidates_narrowed"] = narrowed2
            st.session_state["rect_step"] = "result"
            st.rerun()
        if skip:
            st.session_state["rect_step"] = "result"
            st.rerun()

    elif step == "result":
        narrowed = st.session_state["rect_candidates_narrowed"]
        if st.session_state.get("rect_turning_point_note"):
            st.info(st.session_state["rect_turning_point_note"])
        if len(narrowed) == 1:
            final = narrowed[0]
            st.success(f"{t('rect_result_single', lang)} **{final.label}（{final.time_range}）**")
            if st.button(t("rect_view_chart_btn", lang)):
                st.session_state["rect_final"] = final
                st.session_state["rect_step"] = "done"
                st.rerun()
        else:
            st.info(t("rect_result_multi", lang, n=len(narrowed)))
            for c in narrowed:
                st.markdown(
                    f'<div class="candidate-box"><b>{c.label}（{c.time_range}）</b><br/>{c.personality_text(lang)}</div>',
                    unsafe_allow_html=True,
                )
            labels = [c.label for c in narrowed]
            pick = st.radio(t("rect_choose_label", lang), labels, index=None)
            if pick is not None and st.button(t("rect_confirm_choice_btn", lang)):
                final = next(c for c in narrowed if c.label == pick)
                st.session_state["rect_final"] = final
                st.session_state["rect_step"] = "done"
                st.rerun()

        if st.button(t("rect_restart_btn", lang)):
            st.session_state["rect_step"] = "input"
            st.session_state.pop("rect_turning_point_note", None)
            st.rerun()

    elif step == "done":
        final = st.session_state["rect_final"]
        st.caption(t("rect_done_caption", lang, label=final.label, time_range=final.time_range))
        render_full_report(final.bc, final.zw, lang)
        if st.button(t("rect_redo_btn", lang)):
            st.session_state["rect_step"] = "input"
            st.session_state["unlocked"] = False
            st.session_state.pop("rect_turning_point_note", None)
            st.rerun()
