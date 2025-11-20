import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config

# ---------------- LOAD API KEY ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="NetDoc AI", layout="wide")

# ---------------- LOGO ----------------
st.image("https://i.imgur.com/NU9cu5S.png", width=180)

# ---------------- TITLE ----------------
st.title("⚡ NetDoc AI — Autonomous Network Documentation Engine")
st.write("Upload configs → AI creates documentation, auditing, topology & exports.")

# ---------------- FILE UPLOAD ----------------
uploaded_files = st.file_uploader(
    "Upload Cisco configs",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

# ---------------- TABS ----------------
overview_tab, audit_tab, topology_tab, export_tab = st.tabs(
    ["📄 Overview", "🛡 Security Audit", "🌐 Topology", "📤 Export"]
)

# ---------------- PROCESS ----------------
if uploaded_files and st.button("Generate Report"):
    combined = ""

    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Analyzing your configs..."):
        result = parse_config(combined)

    st.session_state["report"] = result
    st.success("Report generated!")

# ---------------- OVERVIEW ----------------
with overview_tab:
    if "report" in st.session_state:
        st.subheader("📄 Parsed Documentation")
        st.json(st.session_state["report"])
    else:
        st.info("Upload configs and click *Generate Report*.")

# ---------------- SECURITY AUDIT (Next Step C-4) ----------------
with audit_tab:
    st.write("Security audit will be enabled in the next step.")

# ---------------- TOPOLOGY TAB (Next Step C-5) ----------------
with topology_tab:
    st.write("Topology visualization will be enabled in the next step.")

# ---------------- EXPORT TAB (Next Step C-6) ----------------
with export_tab:
    st.write("Export options coming soon.")
