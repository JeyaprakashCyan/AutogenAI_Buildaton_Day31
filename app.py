import streamlit as st
from src.pipeline import answer, AGENT_TO_DEPT
from src.agents import route_agent

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Support Hub",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Styling - customer/employee service portal
# ------------------------------------------------------------
st.markdown(
    """
<style>
/* ---------- Global ---------- */
:root {
    --navy: #0b1f3a;
    --blue: #1463ff;
    --blue-dark: #0c4ed8;
    --blue-soft: #eef5ff;
    --text: #172033;
    --muted: #6f7c91;
    --border: #e6ebf2;
    --surface: #ffffff;
    --surface-2: #f7f9fc;
    --success: #0c9b6d;
}

.stApp {
    background: #f5f7fb;
    color: var(--text);
}

.block-container {
    max-width: 1280px;
    padding: 1.35rem 2rem 7rem 2rem;
}

/* Hide Streamlit chrome that is not useful in a support portal */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

/* ---------- Sidebar / navigation ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1f3a 0%, #103c7d 56%, #1463ff 100%);
    border-right: 0;
}

section[data-testid="stSidebar"] > div {
    padding: 1.1rem 1rem;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 8px 22px 8px;
}

.brand-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.25);
    font-weight: 800;
    font-size: 15px;
    letter-spacing: .4px;
}

.brand-title {
    font-size: 18px;
    font-weight: 800;
    line-height: 1.15;
}

.brand-subtitle {
    font-size: 11px;
    opacity: .68;
    margin-top: 3px;
}

.nav-heading {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: .6;
    margin: 12px 8px 8px 8px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 11px;
    margin: 4px 0;
    border-radius: 10px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.06);
    font-size: 13px;
}

.nav-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #8eb8ff;
    flex: 0 0 auto;
}

.status-card {
    margin-top: 20px;
    padding: 14px;
    border-radius: 12px;
    background: rgba(0,0,0,.14);
    border: 1px solid rgba(255,255,255,.12);
}

.status-line {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #5ee0ad;
    box-shadow: 0 0 0 4px rgba(94,224,173,.13);
}

.sidebar-note {
    font-size: 10px;
    line-height: 1.55;
    opacity: .58;
    margin-top: 8px;
}

/* ---------- Top bar ---------- */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 2px 18px 2px;
}

.breadcrumb {
    color: var(--muted);
    font-size: 12px;
}

.breadcrumb strong {
    color: var(--text);
}

.online-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    border-radius: 999px;
    background: #ecfbf5;
    color: #087653;
    border: 1px solid #ccefe1;
    font-size: 11px;
    font-weight: 700;
}

.online-pill span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #11a873;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    border-radius: 22px;
    background: linear-gradient(120deg, #0b1f3a 0%, #1254b9 58%, #1463ff 100%);
    box-shadow: 0 18px 40px rgba(18, 67, 140, .17);
    color: white;
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -60px;
    top: -90px;
    border-radius: 50%;
    background: rgba(255,255,255,.08);
}

.hero-kicker {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    opacity: .72;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero h1 {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: clamp(1.8rem, 3vw, 2.7rem);
    line-height: 1.1;
    font-weight: 800;
}

.hero p {
    position: relative;
    z-index: 1;
    max-width: 720px;
    margin: 10px 0 0 0;
    color: #dceaff;
    font-size: 14px;
    line-height: 1.6;
}

/* ---------- Quick help cards ---------- */
.section-title {
    margin: 25px 0 10px 0;
    font-size: 16px;
    font-weight: 800;
    color: var(--text);
}

.section-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 12px;
}

div.stButton > button {
    width: 100%;
    min-height: 92px;
    border: 1px solid var(--border);
    border-radius: 15px;
    background: white;
    color: var(--text);
    text-align: left;
    box-shadow: 0 5px 18px rgba(25, 44, 74, .05);
    transition: all .18s ease;
    padding: 14px 15px;
}

div.stButton > button:hover {
    border-color: #b9d0ff;
    background: #fbfdff;
    box-shadow: 0 10px 24px rgba(20, 99, 255, .10);
    transform: translateY(-1px);
}

div.stButton > button p {
    white-space: pre-line;
    line-height: 1.45;
}

/* ---------- Chat area ---------- */
.chat-shell {
    margin-top: 22px;
    padding: 4px 0;
}

[data-testid="stChatMessage"] {
    border: 0 !important;
    background: transparent !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}

[data-testid="stChatMessageContent"] {
    max-width: 820px;
    border-radius: 17px;
    padding: 14px 17px !important;
    border: 1px solid var(--border);
    box-shadow: 0 5px 18px rgba(25, 44, 74, .04);
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: #eaf2ff !important;
    border-color: #d8e7ff !important;
    margin-left: auto;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background: #ffffff !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: var(--text) !important;
    line-height: 1.65;
}

[data-testid="stChatMessage"] [data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
    font-size: 11px !important;
}

/* ---------- Source metadata ---------- */
.meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 8px;
}

.meta-pill {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 999px;
    background: #f1f4f8;
    color: #657286;
    border: 1px solid #e3e8ef;
    font-size: 10px;
    font-weight: 700;
}

/* ---------- Welcome state ---------- */
.welcome {
    margin: 22px auto 8px auto;
    max-width: 760px;
    text-align: center;
    padding: 28px 20px;
}

.welcome-icon {
    width: 62px;
    height: 62px;
    margin: 0 auto 13px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    background: #eaf2ff;
    color: var(--blue);
    font-weight: 900;
    font-size: 18px;
}

.welcome h2 {
    margin: 0;
    color: var(--text);
    font-size: 24px;
}

.welcome p {
    margin: 8px auto 0 auto;
    color: var(--muted);
    font-size: 13px;
    max-width: 590px;
    line-height: 1.6;
}

/* ---------- Input ---------- */
[data-testid="stChatInput"] {
    background: rgba(245,247,251,.96);
    padding-top: 8px;
}

[data-testid="stChatInput"] > div {
    border: 1px solid #dfe6ef !important;
    border-radius: 16px !important;
    background: #ffffff !important;
    box-shadow: 0 12px 30px rgba(25, 44, 74, .10);
}

[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background: #ffffff !important;
    font-size: 13px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8995a6 !important;
}

/* ---------- Expander / evidence ---------- */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: #fbfcfe !important;
}

/* ---------- Mobile ---------- */
@media (max-width: 900px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .hero { padding: 25px 22px; }
    .hero h1 { font-size: 1.9rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
DEPT_ICONS = {
    "IT_Service_Desk_Agent": "IT",
    "Product_Client_Success_Agent": "PS",
    "People_Ops_HR_Policy_Agent": "HR",
    "Talent_Management_Growth_Agent": "TM",
    "Business_Ops_Corporate_Agent": "BO",
}

QUICK_ACTIONS = [
    ("IT Service", "IT", "VPN, password, account access or software issue"),
    ("HR & Leave", "HR", "Leave, benefits, holidays and employee policies"),
    ("Performance", "TM", "Appraisal, reviews, promotion and career growth"),
    ("Products", "PS", "Product features, bugs, releases and onboarding"),
]


def agent_label(agent_name: str) -> str:
    return agent_name.replace("_", " ").replace(" Agent", "")


def run_query(query: str):
    """Run the existing AutoGen -> RAG/Web pipeline without changing backend logic."""
    selected = route_agent(query)
    result = answer(query, selected)
    result["selected_agent"] = selected
    return result


# ------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-logo">AI</div>
            <div>
                <div class="brand-title">Support Hub</div>
                <div class="brand-subtitle">Employee & Customer Services</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-heading">Support teams</div>', unsafe_allow_html=True)
    for agent in AGENT_TO_DEPT:
        icon = DEPT_ICONS.get(agent, "AI")
        label = agent_label(agent)
        st.markdown(
            f'<div class="nav-item"><span class="nav-dot"></span><span><b>{icon}</b>&nbsp;&nbsp;{label}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="status-card">
            <div class="status-line"><span class="status-dot"></span><b>Support system online</b></div>
            <div class="sidebar-note">
                Guardrails → AutoGen routing → FAISS RAG → hybrid reranking → web fallback → specialist response
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("＋  Start a new conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ------------------------------------------------------------
# Main header
# ------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
        <div class="breadcrumb">Support Portal &nbsp; / &nbsp; <strong>AI Assistant</strong></div>
        <div class="online-pill"><span></span> Online</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Intelligent service desk</div>
        <h1>How can we help you today?</h1>
        <p>
            Ask a question about IT, products, HR policies, career growth or business operations.
            The right specialist is selected automatically and answers are grounded in the internal knowledge base first.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Quick actions
# ------------------------------------------------------------
st.markdown('<div class="section-title">Popular support topics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Choose a topic or type your own question below.</div>', unsafe_allow_html=True)

cols = st.columns(4, gap="medium")
for col, (title, icon, description) in zip(cols, QUICK_ACTIONS):
    with col:
        if st.button(f"{icon}  {title}\n{description}", key=f"quick_{title}", use_container_width=True):
            st.session_state.pending_query = description
            st.rerun()

# ------------------------------------------------------------
# Chat history
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome">
            <div class="welcome-icon">AI</div>
            <h2>Your support assistant is ready</h2>
            <p>
                Get policy answers, troubleshoot issues, understand products,
                check appraisal guidance, or ask about business processes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

for m in st.session_state.messages:
    avatar = ":material/person:" if m["role"] == "user" else ":material/smart_toy:"
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])
        if m.get("mode") and m["role"] == "assistant":
            agent = m.get("agent", "Specialist")
            mode = m["mode"]
            st.markdown(
                f'<div class="meta-row"><span class="meta-pill">{agent_label(agent)}</span><span class="meta-pill">{mode}</span></div>',
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------
# Input - keep Streamlit's native chat input for accessibility and
# reliable bottom anchoring. This is also the supported chat pattern.
# ------------------------------------------------------------
query = st.chat_input("Ask anything about your support request...", max_chars=2000)

# A quick-action click can prefill/submit a query on the next rerun.
if not query and st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = ""

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        with st.status("Working on your request...", expanded=False) as status:
            try:
                result = run_query(query)
                status.update(label="Response ready", state="complete")
            except Exception as exc:
                status.update(label="Unable to complete request", state="error")
                result = {
                    "answer": "I’m sorry, but I couldn’t process that request right now. Please try again.",
                    "mode": "ERROR",
                    "sources": [],
                    "selected_agent": "Support Agent",
                    "error": str(exc),
                }

        st.markdown(result["answer"])
        selected = result.get("selected_agent", "Support Agent")
        mode = result.get("mode", "UNKNOWN")
        st.markdown(
            f'<div class="meta-row"><span class="meta-pill">{agent_label(selected)}</span><span class="meta-pill">{mode}</span></div>',
            unsafe_allow_html=True,
        )

        if result.get("sources") and mode == "RAG":
            with st.expander("View supporting knowledge", expanded=False):
                for source in result["sources"]:
                    st.markdown(
                        f"**{source['source']} · page {source['page']} · relevance {source['rerank_score']:.3f}**"
                    )
                    st.write(source["text"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "mode": result.get("mode", "UNKNOWN"),
            "agent": result.get("selected_agent", "Support Agent"),
        }
    )
