# ============================================================
#  NetDoc AI — Upload & Audit Page (Full Professional Version)
# ============================================================

import streamlit as st
from main import run_security_audit, generate_topology_mermaid, export_all_formats


def upload_and_audit_page():
    st.title("📤 Upload & Audit Configuration")

    st.markdown("""
Upload any **Cisco / Fortinet / Generic** router or switch configuration file.

NetDoc AI will automatically:
1. Run a **security audit**
2. Generate a **Mermaid topology diagram**
3. Provide an optional **ZIP export**
""")

    uploaded = st.file_uploader(
        "Upload Configuration File",
        type=["txt", "cfg", "conf"],
        help="Supported formats: .txt, .cfg, .conf"
    )

    if not uploaded:
        st.info("Drag & drop a configuration file above to begin.")
        return

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------
    try:
        config_text = uploaded.read().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    # --------------------------------------------------------
    # SECURITY AUDIT
    # --------------------------------------------------------
    st.subheader("🔍 Audit Result")

    audit = run_security_audit(config_text)

    col1, col2, col3 = st.columns(3)
    col1.metric("Line Count", audit.get("line_count"))
    col2.metric("Risk Score (0–100)", audit.get("risk_score"))
    col3.metric("Enable Secret Used?", "Yes" if audit.get("contains_enable_secret") else "No")

    with st.expander("Show full audit JSON"):
        st.json(audit)

    # --------------------------------------------------------
    # TOPOLOGY
    # --------------------------------------------------------
    st.subheader("🗺️ Topology Diagram")

    topology = generate_topology_mermaid(config_text)

    st.markdown("Copy/paste this Mermaid diagram anywhere:")
    st.code(topology, language="mermaid")

    # --------------------------------------------------------
    # EXPORT ZIP
    # --------------------------------------------------------
    st.subheader("📦 Export Results")

    if st.button("Generate ZIP Bundle"):
        zip_bytes = export_all_formats(config_text, audit, topology)
        st.download_button(
            label="Download results.zip",
            data=zip_bytes,
            file_name="netdoc_ai_results.zip",
            mime="application/zip"
        )
