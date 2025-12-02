# ===============================================================
#  NetDoc AI — Audit Page (Streamlit)
# ===============================================================

import streamlit as st
from utils.parser import parse_config
from audit_engine import run_security_audit
from main import generate_topology_mermaid, export_all_formats


def audit_page():
    st.title("🔎 Configuration Security Audit")

    uploaded = st.file_uploader(
        "Upload Configuration File",
        type=["txt", "cfg", "conf"]
    )

    if uploaded:
        config_text = uploaded.read().decode()

        # -------------------------------------------------------
        # FIX: parse_config now returns pure string
        # -------------------------------------------------------
        parsed = parse_config(config_text)   # returns string
        raw = parsed                         # the actual config text

        audit_result = run_security_audit(raw)
        topology = generate_topology_mermaid(raw)
        exports = export_all_formats(audit_result, topology)

        # ---------------- DISPLAY AUDIT -----------------------
        st.subheader("🛡 Security Audit Result")
        st.json(audit_result)

        # ---------------- TOPOLOGY GRAPH ----------------------
        st.subheader("🌐 Topology Diagram")
        st.markdown(f"```mermaid\n{topology}\n```")

        # ---------------- EXPORT BUTTONS ----------------------
        st.subheader("📦 Export Results")
        st.download_button("Download JSON", exports["json"], file_name="audit.json")
        st.download_button("Download Markdown", exports["markdown"], file_name="audit.md")
        st.download_button("Download TXT", exports["txt"], file_name="audit.txt")
        st.download_button("Download HTML", exports["html"], file_name="audit.html")

    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
