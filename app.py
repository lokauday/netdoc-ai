import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config

# ------------------------------
#  Load API Key
# ------------------------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ------------------------------
#  BRANDING CONFIG
# ------------------------------
BRAND_LOGO = "https://i.imgur.com/tH9yO4M.png"   # Replace with your real logo later
BRAND_NAME = "⚡ NetDoc AI — Autonomous Network Documentation Engine"
BRAND_FOOTER = "© 2025 NetDoc AI — All Rights Reserved • Built by Uday"

# ------------------------------
#  STREAMLIT PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="NetDoc AI",
    layout="wide",
    page_icon="⚡"
)

# ------------------------------
#  BRANDING HEADER
# ------------------------------
col1, col2 = st.columns([1, 5])
with col1:
    st.image(BRAND_LOGO, width=90)

with col2:
    st.markdown(
        f"""
        <h1 style="margin-bottom:0;">{BRAND_NAME}</h1>
        <p style="font-size:18px; margin-top:5px;">
            Upload configs → AI creates documentation, topology, audits & more.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ------------------------------
#  UPLOAD SECTION
# ------------------------------
uploaded_files = st.file_uploader(
    "Upload configuration files (TXT, LOG, CFG)",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

# ------------------------------
#  TABS: Overview / Audit / Topology / Export
# ------------------------------
tab_overview, tab_audit, tab_topology, tab_export = st.tabs(
    ["📄 Overview", "🛡 Security Audit", "🌐 Topology", "📦 Export"]
)

# -------------- PROCESS FILES ---------------
if uploaded_files:

    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Analyzing network configuration…"):
        parsed = parse_config(combined)

    # ---------------- OVERVIEW TAB ----------------
    with tab_overview:
        st.subheader("📄 Parsed Documentation")
        st.json(parsed)

    # ---------------- AUDIT TAB ----------------
    with tab_audit:
        st.subheader("🛡 Security Audit (Coming Next Step)")
        st.info("AI security checks will be added in Step C.")

    # ---------------- TOPOLOGY TAB ----------------
    with tab_topology:
        st.subheader("🌐 Auto-Generated Topology")
        topo = parsed.get("ascii_topology", "")
        if topo:
            st.code(topo, language="text")
        else:
            st.warning("No topology information generated yet.")

    # ---------------- EXPORT TAB ----------------
    with tab_export:
        st.subheader("📦 Export Options")
        st.info("PDF / DOCX / HTML exports arrive in Step C.")

# ------------------------------
#  FOOTER
# ------------------------------
st.markdown(
    f"""
    <br><br><center style="opacity:0.6;">{BRAND_FOOTER}</center>
    """,
    unsafe_allow_html=True
)
