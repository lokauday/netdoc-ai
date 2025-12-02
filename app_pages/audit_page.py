
---

# ✅ **2️⃣ Replace: `app_pages/audit_page.py` (Correct import + logic)**

```python
# ===============================================================
#  NetDoc AI — Audit Page
# ===============================================================

import streamlit as st
from utils.parser import parse_config
from audit_engine import run_security_audit
from topology_engine import generate_topology_mermaid
from exports.exporter import export_all_formats


def audit_page():
    st.title("🔎 Security Audit")

    uploaded = st.file_uploader("Upload Configuration File", type=["txt", "cfg", "conf"])

    if uploaded:
        raw_text = uploaded.read().decode()

        parsed = parse_config(raw_text)

        # Extract safe raw text
        raw_content = parsed["raw"] if isinstance(parsed, dict) else raw_text

        # Run audit
        audit_result = run_security_audit(parsed)

        # Generate topology
        topology = generate_topology_mermaid(parsed)

        # Generate exports
        exports = export_all_formats(audit_result, topology)

        st.subheader("Audit Result")
        st.json(audit_result)

        st.subheader("Topology")
        st.markdown(f"```mermaid\n{topology}\n```")

        st.subheader("Export Files")
        st.download_button("Download JSON", exports["json"], file_name="audit.json")
        st.download_button("Download Markdown", exports["markdown"], file_name="audit.md")
        st.download_button("Download TXT", exports["txt"], file_name="audit.txt")
        st.download_button("Download HTML", exports["html"], file_name="audit.html")

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"
        st.rerun()
