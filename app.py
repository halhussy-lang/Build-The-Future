import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="CivicLens AI",
    page_icon="🇮🇳",
    layout="centered"
)

st.title("🇮🇳 CivicLens AI")
st.caption("Making Indian government services understandable for everyone")

# Sidebar
st.sidebar.header("About CivicLens AI")
st.sidebar.write(
    "CivicLens AI helps Indian citizens understand government schemes "
    "and convert civic issues into structured complaints using AI."
)

# API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found. Please set it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Golden Prompt
SYSTEM_PROMPT = """
You are CivicLens AI, an expert civic assistant for Indian public services.

Your objectives:
1. Explain Indian government schemes in simple, non-technical language.
2. Ask only essential follow-up questions.
3. Determine eligibility clearly and honestly.
4. Convert citizen issues into structured complaint drafts when requested.
5. Provide step-by-step next actions.

Rules:
- Avoid bureaucratic language.
- Use bullet points and numbered steps.
- Be empathetic, inclusive, and citizen-first.
- State limitations clearly when information is uncertain.

Your priority is clarity, accessibility, and real-world usefulness for Indian citizens.
"""

# Tabs
tab1, tab2 = st.tabs(["📜 Government Schemes", "🛠 Civic Complaints"])

# ---- TAB 1: SCHEMES ----
with tab1:
    st.subheader("Ask about a government scheme")
    scheme_query = st.text_area(
        "Example: Am I eligible for PMAY housing scheme?",
        height=120
    )

    if st.button("Check Scheme Details"):
        if scheme_query.strip():
            with st.spinner("Analyzing scheme details..."):
                response = model.generate_content(
                    SYSTEM_PROMPT + "\n\nUser query:\n" + scheme_query
                )
                st.markdown(response.text)
        else:
            st.warning("Please enter a scheme-related question.")

# ---- TAB 2: COMPLAINTS ----
with tab2:
    st.subheader("Describe your civic issue")
    complaint_query = st.text_area(
        "Example: Garbage not collected for 10 days in my area",
        height=120
    )

    if st.button("Generate Complaint Draft"):
        if complaint_query.strip():
            with st.spinner("Drafting complaint..."):
                response = model.generate_content(
                    SYSTEM_PROMPT
                    + "\n\nConvert the following issue into a structured complaint:\n"
                    + complaint_query
                )
                st.markdown(response.text)
        else:
            st.warning("Please describe your civic issue.")
