import streamlit as st
import requests

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
API_URL = "http://127.0.0.1:8001/chat"

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InsyteAI",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for key, default in [
    ("user_msg", ""),
    ("bot_msg", ""),
    ("is_error", False),
    ("has_response", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
#  HELPER – call backend API
# ─────────────────────────────────────────────
def call_api(query: str) -> tuple[str, bool]:
    try:
        resp = requests.post(API_URL, json={"user_input": query}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            reply = data.get("generated_sql") or data.get("query") or data.get("answer") or str(data)
        else:
            reply = str(data)
        return reply, False
    except Exception:
        return "Something went wrong. Please try again.", True

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── App background ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(160deg, #E8F2FF 0%, #F2F7FF 45%, #FFFFFF 100%) !important;
    min-height: 100vh;
}

/* ── Remove default Streamlit padding & chrome ── */
#MainMenu, footer, header { visibility: hidden; height: 0; }
[data-testid="stToolbar"] { display: none; }

[data-testid="stAppViewContainer"] > section > div.block-container {
    padding: 0 0 2rem 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* ══════════════════════════
   NAV
══════════════════════════ */
.insyte-nav {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 2rem;
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(180,210,245,0.45);
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.nav-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1D4ED8, #3B82F6);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.nav-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.02em;
}
.nav-title span { color: #2563EB; }
.nav-links {
    display: flex;
    align-items: center;
    gap: 1.8rem;
    font-size: 0.875rem;
    font-weight: 500;
}
.nav-links a {
    color: #475569;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    transition: color 0.15s;
}
.nav-links a:hover { color: #2563EB; }

/* ══════════════════════════
   PAGE WRAPPER
══════════════════════════ */
.page-wrap {
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

/* ══════════════════════════
   HERO
══════════════════════════ */
.hero {
    text-align: center;
    padding: 4.5rem 0 2.5rem;
}
.hero h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.035em;
    line-height: 1.15;
    margin: 0 0 1rem;
}
.hero p {
    font-size: clamp(0.9rem, 2.2vw, 1.05rem);
    color: #475569;
    font-weight: 400;
    line-height: 1.65;
    max-width: 520px;
    margin: 0 auto;
}

/* ══════════════════════════
   INPUT SECTION
   Streamlit columns sit inside the glass card.
   We target the column wrappers directly so the
   input + button stay on one flex row.
══════════════════════════ */
.input-outer {
    margin: 2.2rem 0 0.5rem;
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(186,215,248,0.65);
    border-radius: 18px;
    box-shadow:
        0 2px 24px rgba(37,99,235,0.07),
        0 1px 3px rgba(0,0,0,0.04),
        inset 0 1px 0 rgba(255,255,255,0.95);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    padding: 6px 6px 6px 16px;
    /* make the internal Streamlit columns form a flex row */
    display: flex;
    align-items: center;
}

/* Streamlit injects a div[data-testid="column"] per column.
   Make the text-input column grow and button column shrink. */
.input-outer [data-testid="column"]:first-child {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    width: auto !important;
}
.input-outer [data-testid="column"]:last-child {
    flex: 0 0 auto !important;
    width: auto !important;
}

/* Strip all Streamlit input chrome */
.input-outer [data-testid="stTextInput"] > div,
.input-outer [data-testid="stTextInput"] > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.input-outer [data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.97rem !important;
    color: #0F172A !important;
    padding: 10px 4px 10px 0 !important;
    caret-color: #2563EB;
    width: 100% !important;
}
.input-outer [data-testid="stTextInput"] input::placeholder {
    color: #94A3B8 !important;
    font-size: 0.95rem !important;
}

/* Generate button */
.input-outer [data-testid="stBaseButton-secondary"],
.input-outer .stButton > button {
    background: linear-gradient(135deg, #CBD5E1 0%, #B0C4D8 100%) !important;
    color: #475569 !important;
    border: none !important;
    border-radius: 13px !important;
    padding: 0 1.2rem !important;
    height: 42px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}
.input-outer [data-testid="stBaseButton-secondary"]:hover:not(:disabled),
.input-outer .stButton > button:hover:not(:disabled) {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.28) !important;
    transform: translateY(-1px) !important;
}
.input-outer [data-testid="stBaseButton-secondary"]:disabled,
.input-outer .stButton > button:disabled {
    opacity: 0.48 !important;
    cursor: default !important;
    transform: none !important;
}

/* ══════════════════════════
   RESPONSE BUBBLES
══════════════════════════ */
.response-area {
    margin-top: 1.6rem;
    padding-bottom: 3rem;
}

.bubble-user-row {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0.9rem;
}
.bubble-user {
    background: linear-gradient(135deg, #1D4ED8, #3B82F6);
    color: #fff;
    border-radius: 16px 16px 3px 16px;
    padding: 0.85rem 1.15rem;
    max-width: 72%;
    font-size: 0.93rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(37,99,235,0.22);
    word-wrap: break-word;
}

.bubble-bot-row {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.bot-avatar {
    width: 32px; height: 32px;
    min-width: 32px;
    background: linear-gradient(135deg, #1D4ED8, #3B82F6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    color: #fff;
    box-shadow: 0 2px 8px rgba(37,99,235,0.22);
}
.bubble-bot {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(186,215,248,0.6);
    border-radius: 3px 16px 16px 16px;
    padding: 0.85rem 1.15rem;
    max-width: 72%;
    font-size: 0.93rem;
    line-height: 1.65;
    color: #0F172A;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 12px rgba(37,99,235,0.05);
    word-wrap: break-word;
}
.bubble-error {
    background: #FFF1F0 !important;
    border-color: #FCA5A5 !important;
    color: #B91C1C !important;
}

/* ══════════════════════════
   FOOTER
══════════════════════════ */
.insyte-footer {
    width: 100%;
    border-top: 1px solid rgba(186,215,248,0.45);
    padding: 1.2rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.73rem;
    font-weight: 500;
    color: #94A3B8;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 2rem;
}
.footer-links { display: flex; gap: 1.6rem; }

/* ══════════════════════════
   RESPONSIVE
══════════════════════════ */
@media (max-width: 600px) {
    .insyte-nav    { padding: 0.8rem 1rem; }
    .nav-links     { display: none; }
    .page-wrap     { padding: 0 0.9rem; }
    .hero          { padding: 3rem 0 2rem; }
    .bubble-user,
    .bubble-bot    { max-width: 88%; }
    .insyte-footer {
        flex-direction: column;
        gap: 0.6rem;
        text-align: center;
        padding: 1rem;
    }
    .footer-links  { gap: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAV
# ─────────────────────────────────────────────
st.markdown("""
<div class="insyte-nav">
  <div class="nav-brand">
    <div class="nav-logo">📊</div>
    <span class="nav-title">Insyte<span>AI</span></span>
  </div>
  <div class="nav-links">
    <a href="#">📈 Analytics</a>
    <a href="#">💬 Support</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE WRAPPER OPEN
# ─────────────────────────────────────────────
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Insyte AI Assistant</h1>
  <p>Enterprise-grade marketing analytics at your fingertips.<br>
     Ask questions about your campaigns, revenue, and trends.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT CARD
#  The .input-outer div is opened, then Streamlit
#  columns are rendered inside it — CSS flex rules
#  override the column widths to keep everything
#  on one row regardless of screen size.
# ─────────────────────────────────────────────
st.markdown('<div class="input-outer">', unsafe_allow_html=True)
col_inp, col_btn = st.columns([6, 1], gap="small")
with col_inp:
    user_input = st.text_input(
        label="query",
        placeholder="e.g. 'Show me conversions for the last LinkedIn campaign'",
        label_visibility="collapsed",
        key="input_field",
    )
with col_btn:
    send_clicked = st.button(
        "Generate ➤",
        disabled=not (user_input and user_input.strip()),
        use_container_width=True,
        key="send_btn",
    )
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RESPONSE AREA
# ─────────────────────────────────────────────
if st.session_state.has_response:
    st.markdown('<div class="response-area">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="bubble-user-row">'
        f'<div class="bubble-user">{st.session_state.user_msg}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    err_cls = " bubble-error" if st.session_state.is_error else ""
    icon = "⚠" if st.session_state.is_error else "📊"
    st.markdown(
        f'<div class="bubble-bot-row">'
        f'<div class="bot-avatar">{icon}</div>'
        f'<div class="bubble-bot{err_cls}">{st.session_state.bot_msg}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE WRAPPER CLOSE
# ─────────────────────────────────────────────
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="insyte-footer">
  <span>© 2026 Insyte AI Analytics</span>
  <div class="footer-links">
    <span>Privacy</span>
    <span>Terms</span>
    <span>Documentation</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ON SEND
# ─────────────────────────────────────────────
if send_clicked and user_input and user_input.strip():
    st.session_state.user_msg = user_input.strip()
    with st.spinner("Analyzing your query…"):
        reply, is_error = call_api(user_input.strip())
    st.session_state.bot_msg = reply
    st.session_state.is_error = is_error
    st.session_state.has_response = True
    st.rerun()