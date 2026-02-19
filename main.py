import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from agents.manager import manager


load_dotenv()


def _extract_text(response) -> str:
    if hasattr(response, "content") and response.content:
        return str(response.content)
    if isinstance(response, str):
        return response
    return str(response)


def _load_api_key_from_secrets() -> bool:
    if os.getenv("OPENAI_API_KEY"):
        return True

    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            os.environ["OPENAI_API_KEY"] = key
            return True
    except Exception:
        return False

    return False


st.set_page_config(
    page_title="Multi-Agentic AI Studio",
    page_icon="AI",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');
    :root {
      --bg-1: #f3f9f7;
      --bg-2: #eef4ff;
      --card: #ffffffcc;
      --ink: #12323a;
      --muted: #537079;
      --accent: #0a8f7a;
      --accent-2: #ff8a3d;
      --border: #d5e7e5;
    }
    html, body, [class*="css"]  {
      font-family: "Manrope", sans-serif;
      color: var(--ink);
    }
    .stApp {
      background:
        radial-gradient(1200px 500px at 10% -10%, #d8fff3 0%, transparent 60%),
        radial-gradient(900px 500px at 95% 0%, #dbe7ff 0%, transparent 60%),
        linear-gradient(120deg, var(--bg-1), var(--bg-2));
    }
    .hero {
      border: 1px solid var(--border);
      background: var(--card);
      backdrop-filter: blur(6px);
      border-radius: 18px;
      padding: 1.2rem 1.2rem 1rem 1.2rem;
      margin-bottom: 1rem;
      box-shadow: 0 12px 30px rgba(18, 50, 58, 0.06);
    }
    .hero h1 {
      margin: 0;
      font-weight: 800;
      letter-spacing: -0.03em;
      font-size: clamp(1.4rem, 3.8vw, 2.4rem);
    }
    .hero p {
      margin: 0.5rem 0 0 0;
      color: var(--muted);
      line-height: 1.5;
    }
    .metric-card {
      border: 1px solid var(--border);
      background: #ffffffd9;
      border-radius: 14px;
      padding: 0.8rem 1rem;
      margin-top: 0.4rem;
    }
    .metric-label {
      color: var(--muted);
      font-size: 0.86rem;
      margin-bottom: 0.2rem;
    }
    .metric-value {
      font-size: 1.1rem;
      font-weight: 700;
    }
    .result-card {
      border: 1px solid #cde4de;
      border-radius: 16px;
      background: #ffffffde;
      padding: 1rem 1rem 0.4rem 1rem;
      box-shadow: 0 8px 20px rgba(18, 50, 58, 0.06);
    }
    .tag {
      display: inline-block;
      padding: 0.22rem 0.6rem;
      border-radius: 999px;
      border: 1px solid #b8ded4;
      background: #e9fff8;
      color: #0a6b5c;
      font-size: 0.75rem;
      margin-right: 0.45rem;
      margin-bottom: 0.55rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
    <div class="hero">
      <h1>Multi-Agentic AI Studio</h1>
      <p>Research, analyze, write, and review in one workflow. Enter a topic and get a polished, structured answer.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_a:
    st.markdown(
        """
        <div class="metric-card">
          <div class="metric-label">Agents</div>
          <div class="metric-value">4 Active</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Runs This Session</div>
          <div class="metric-value">{len(st.session_state.history)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_c:
    key_ok = _load_api_key_from_secrets()
    key_state = "Configured" if key_ok else "Missing"
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">OpenAI Key</div>
          <div class="metric-value">{key_state}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.markdown("### Project Control")
    st.write("Use this app to run your multi-agent pipeline from a clean hosted UI.")
    st.markdown("`Researcher` `Analyst` `Writer` `Reviewer`")
    if st.button("Clear Session History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

st.markdown("### Ask Your Multi-Agent Team")
query = st.text_area(
    "Topic or question",
    placeholder="Example: Compare top AI agent frameworks for startup MVPs in 2026 with pros/cons and recommendation.",
    height=130,
    label_visibility="collapsed",
)
run_clicked = st.button("Generate Response", type="primary", use_container_width=True)

if run_clicked:
    if not query.strip():
        st.warning("Please enter a topic before generating a response.")
    elif not key_ok:
        st.error("OPENAI_API_KEY is missing. Add it to Streamlit secrets or your .env file.")
    else:
        with st.spinner("Coordinating agents and drafting final output..."):
            try:
                raw_response = manager.run(query.strip())
                output = _extract_text(raw_response)
                st.session_state.history.insert(
                    0,
                    {
                        "query": query.strip(),
                        "output": output,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                )
            except Exception as exc:
                st.error(f"Error while running agents: {exc}")

if st.session_state.history:
    latest = st.session_state.history[0]

    st.markdown("### Latest Result")
    st.markdown(
        """
        <span class="tag">Multi-Agent Output</span>
        <span class="tag">Markdown Ready</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(latest["output"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="Download Latest Result (.md)",
        data=latest["output"],
        file_name="multi_agent_output.md",
        mime="text/markdown",
        use_container_width=True,
    )

    with st.expander("Show Past Runs"):
        for item in st.session_state.history[1:]:
            st.markdown(f"**{item['timestamp']}**")
            st.markdown(f"**Query:** {item['query']}")
            st.markdown(item["output"])
            st.divider()
