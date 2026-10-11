"""
beta_notice.py - shows the beta statement under the app title (en / id / zh).
Edit the text below, then restart Streamlit. No other logic.
"""

BETA_TEXT = {
    "en": ("<b>Beta</b> &middot; This app is in testing and free to use. Results are for self-reflection, "
           "not predictions, and features may change. Paid plans may be introduced later."),
    "id": ("<b>Beta</b> &middot; Aplikasi ini sedang diuji dan gratis digunakan. Hasilnya untuk refleksi diri, "
           "bukan ramalan, dan fitur dapat berubah. Paket berbayar mungkin diperkenalkan nanti."),
    "zh": ("<b>測試版</b> &middot; 本應用正在測試中，目前免費使用。結果僅供自我反思，並非預測，"
           "功能可能變動。日後可能推出付費方案。"),
}


def render_beta_notice(st, lang):
    text = BETA_TEXT.get(lang, BETA_TEXT["en"])
    st.markdown('<div class="info-card">%s</div>' % text, unsafe_allow_html=True)
