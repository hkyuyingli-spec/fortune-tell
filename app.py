import datetime
import streamlit as st

from calendar_engine import BirthChart
from ziwei_engine import ZiWeiChart
import interpretation as interp
import rectification as rect

st.set_page_config(page_title="命盤 · Destiny Chart", page_icon="🔮", layout="centered")

st.markdown("""
<style>
:root {
    --ink:#14182A; --paper:#EFE7D8; --cinnabar:#B23A2E; --gold:#C9A15A; --jade:#4B7A6D;
}
.stApp { background: var(--ink); }
h1, h2, h3 { font-family: "Noto Serif TC", serif !important; color: var(--gold) !important; }
.block-container { max-width: 720px; }
.free-card, .paid-card, .rect-card {
    background: var(--paper); color: #23262F; border-radius: 6px;
    padding: 24px 28px; margin-bottom: 18px;
}
.paid-card { border-left: 4px solid var(--cinnabar); }
.rect-card { border-left: 4px solid var(--jade); }
.palace-row { border-bottom: 1px dotted rgba(35,38,47,0.25); padding: 10px 0; }
.disclaimer { color: #C9A15A; font-size: 12.5px; margin-top: 18px; line-height:1.6; }
.candidate-box { border: 1px solid rgba(35,38,47,0.2); border-radius: 4px; padding: 10px 14px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("命盤 · Destiny Chart")
st.caption("紫微斗數 + 八字 命盤產生器 — 免費看命盤結構，付費解鎖完整解讀")


def render_full_report(bc: BirthChart, zw: ZiWeiChart):
    """Shared rendering for a resolved chart (whether time was known
    upfront, or arrived at via 定盤 rectification)."""
    pillars = bc.four_pillars.as_dict()

    st.markdown('<div class="free-card">', unsafe_allow_html=True)
    st.subheader("免費 · 命盤概覽")
    st.markdown(interp.free_tier_summary(pillars, pillars["day"][0], zw))
    st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.get("unlocked"):
        st.info("完整報告包含：十二宮完整星曜、每個宮位解讀、十年大限排程、今年流年宮位")
        if st.button("🔓 解鎖完整報告 Unlock Full Report"):
            st.session_state["unlocked"] = True
            st.rerun()
    else:
        st.markdown('<div class="paid-card">', unsafe_allow_html=True)
        st.subheader("付費 · 完整命盤解讀")

        current_year = datetime.date.today().year
        rows, current_palace = interp.paid_tier_report(zw, current_year)

        if current_palace:
            st.markdown(f"**{current_year} 年流年宮位：{current_palace}**")

        for row in rows:
            st.markdown(
                f"""<div class="palace-row">
                <b>{row['palace']}</b>（{row['meaning']}）— {row['stem_branch']}<br/>
                主星：{row['stars']}<br/>
                {row['blurb']}<br/>
                <span style="color:#8a7b6c;">大限：{row['decade_range']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<p class="disclaimer">此命盤結構（十二宮、十四主星、五行局、大限）依紫微斗數傳統排盤規則計算，'
        '並經過與開源排盤工具（iztro）交叉驗證。目前尚未納入輔星、四化飛星與逐月/逐日流曜，屬於下一階段功能。'
        '本報告僅供自我探索與參考，非科學預測，請勿作為人生重大決策的唯一依據。</p>',
        unsafe_allow_html=True,
    )


mode = st.radio(
    "你知道確切的出生時間嗎？",
    ["know_time", "unknown_time"],
    format_func=lambda m: "✅ 我知道確切的出生時間" if m == "know_time" else "❓ 我不確定 / 不知道出生時間",
    horizontal=False,
)

# Reset the flow's state if the mode changes
if st.session_state.get("mode") != mode:
    st.session_state["mode"] = mode
    st.session_state.pop("chart_input", None)
    st.session_state.pop("rect_step", None)
    st.session_state.pop("rect_candidates", None)
    st.session_state["unlocked"] = False

# ============================== KNOW TIME ==============================
if mode == "know_time":
    with st.form("birth_form"):
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input("出生日期（陽曆）", value=datetime.date(1990, 1, 1),
                                        min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2035, 12, 31))
        with col2:
            birth_time = st.time_input("出生時間", value=datetime.time(12, 0))
        gender = st.radio("性別", ["male", "female"], format_func=lambda g: "男" if g == "male" else "女", horizontal=True)
        submitted = st.form_submit_button("排盤 Reveal Chart")

    if submitted:
        st.session_state["chart_input"] = (birth_date, birth_time, gender)
        st.session_state["unlocked"] = False

    if "chart_input" in st.session_state:
        birth_date, birth_time, gender = st.session_state["chart_input"]
        bc = BirthChart(birth_date.year, birth_date.month, birth_date.day, birth_time.hour, birth_time.minute)
        zw = ZiWeiChart(bc, gender)
        render_full_report(bc, zw)

# ============================== UNKNOWN TIME: 定盤 ==============================
else:
    st.markdown(
        '<div class="rect-card">紫微斗數的命宮、身宮、十四主星都是由「出生時辰」直接決定的 —— '
        '沒有時辰，命盤不是「比較不準」，而是<b>無法唯一決定</b>：同一天出生、不同時辰，'
        '可能對應到完全不同的命盤。以下用傳統「定盤」的方式，透過幾個問題幫你縮小範圍。</div>',
        unsafe_allow_html=True,
    )

    step = st.session_state.get("rect_step", "input")

    if step == "input":
        with st.form("rect_form"):
            col1, col2 = st.columns(2)
            with col1:
                r_date = st.date_input("出生日期（陽曆）", value=datetime.date(1990, 1, 1),
                                        min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2035, 12, 31))
            with col2:
                r_gender = st.radio("性別", ["male", "female"], format_func=lambda g: "男" if g == "male" else "女", horizontal=True)
            go = st.form_submit_button("開始定盤 Start Rectification")
        if go:
            candidates = rect.generate_candidates(r_date.year, r_date.month, r_date.day, r_gender)
            st.session_state["rect_candidates"] = candidates
            st.session_state["rect_step"] = "personality"
            st.rerun()

    elif step == "personality":
        candidates = st.session_state["rect_candidates"]
        pq = rect.personality_question(candidates)
        st.subheader("第一步：哪一段個性描述最像你？")
        options = [text for text, _ in pq]
        choice = st.radio("選一個最接近的（不用完全符合，選最像的就好）", options, index=None)
        if choice is not None and st.button("下一步"):
            chosen_idxs = dict(pq)[choice]
            narrowed = rect.narrow_by_personality(candidates, chosen_idxs)
            st.session_state["rect_candidates_narrowed"] = narrowed
            st.session_state["rect_step"] = "turning_point"
            st.rerun()

    elif step == "turning_point":
        narrowed = st.session_state["rect_candidates_narrowed"]
        st.subheader("第二步：人生中一個明顯的轉折點，大概發生在幾歲？")
        st.caption("例如：換跑道、重大決定、明顯的順逆變化。不確定的話可以按「跳過」。")
        age = st.slider("大約年齡", 5, 60, 25)
        col1, col2 = st.columns(2)
        with col1:
            confirm = st.button("確認年齡")
        with col2:
            skip = st.button("跳過此題")
        if confirm:
            narrowed2 = rect.narrow_by_turning_point(narrowed, age)
            st.session_state["rect_candidates_narrowed"] = narrowed2
            st.session_state["rect_step"] = "result"
            st.rerun()
        if skip:
            st.session_state["rect_step"] = "result"
            st.rerun()

    elif step == "result":
        narrowed = st.session_state["rect_candidates_narrowed"]
        if len(narrowed) == 1:
            final = narrowed[0]
            st.success(f"根據你的回答，最可能的時辰是：**{final.label}（{final.time_range}）**")
            if st.button("查看完整命盤"):
                st.session_state["rect_final"] = final
                st.session_state["rect_step"] = "done"
                st.rerun()
        else:
            st.info(f"縮小到 {len(narrowed)} 個可能的時辰，請憑直覺選一個最像你的：")
            for c in narrowed:
                st.markdown(
                    f'<div class="candidate-box"><b>{c.label}（{c.time_range}）</b><br/>{c.personality_text()}</div>',
                    unsafe_allow_html=True,
                )
            labels = [c.label for c in narrowed]
            pick = st.radio("選擇", labels, index=None)
            if pick is not None and st.button("確認選擇"):
                final = next(c for c in narrowed if c.label == pick)
                st.session_state["rect_final"] = final
                st.session_state["rect_step"] = "done"
                st.rerun()

        if st.button("重新開始定盤"):
            st.session_state["rect_step"] = "input"
            st.rerun()

    elif step == "done":
        final = st.session_state["rect_final"]
        st.caption(f"以下命盤基於推定時辰：{final.label}（{final.time_range}）— 如未來確認實際時辰，結果可能不同。")
        render_full_report(final.bc, final.zw)
        if st.button("重新定盤"):
            st.session_state["rect_step"] = "input"
            st.session_state["unlocked"] = False
            st.rerun()
