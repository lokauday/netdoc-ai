import streamlit as st
from utils.parser import parse_config
from audit_engine import run_security_audit
from topology_engine import generate_topology_mermaid
from export_engine import export_all_formats
import time

# ===============================================================
#  PROFESSIONAL UPLOAD & AUDIT PAGE
# ===============================================================

def audit_page():

    st.markdown("""
        <style>
            .upload-box {
                border: 2px dashed #5c6bc0;
                padding: 40px;
                border-radius: 14px;
                text-align: center;
                color: #ddd;
                transition: 0.3s ease;
            }
            .upload-box:hover {
                border-color: #8796ff;
                background: rgba(92,107,192,0.08);
            }
            .section-title {
                font-size: 22px;
                font-weight: 700;
                margin-top: 30px;
                margin-bottom: 10px;
            }
            .result-box {
                background: #23262d;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #343840;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📤 Upload Configuration & Run Audit")

    # -----------------------------------------------------------
    # DRAG & DROP UPLOAD BOX
    # -----------------------------------------------------------
    st.markdown("<div class='upload-box'>📄 Drag & Drop a config file here</div>",
                unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=["txt", "cfg", "conf"])

    if uploaded:
        st.success("File uploaded successfully!")

        config_text = uploaded.read().decode()

        # -----------------------------------------
        # Fake progress bar for UX
        # -----------------------------------------
        with st.spinner("Processing configuration..."):
            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.005)
                progress.progress(i)

        # -----------------------------------------
        # Parse + Audit
        # -----------------------------------------
        parsed = parse_config(config_text)
        audit_result = run_security_audit(parsed["raw"])
        topology = generate_topology_mermaid(parsed["raw"])
        exports = export_all_formats(audit_result, topology)

        # -----------------------------------------------------------
        # AUDIT RESULTS SECTION
        # -----------------------------------------------------------
        st.markdown("<div class='section-title'>🛡 Security Audit Results</div>",
                    unsafe_allow_html=True)

        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.json(audit_result)
        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------------------------------------
        # TOPOLOGY SECTION
        # -----------------------------------------------------------
        st.markdown("<div class='section-title'>🌐 Topology Map</div>",
                    unsafe_allow_html=True)

        st.markdown(f"""
            <div class='result-box'>
                <pre class='mermaid'>{topology}</pre>
            </div>
        """, unsafe_allow_html=True)

        # -----------------------------------------------------------
        # EXPORT SECTION
        # -----------------------------------------------------------
        st.markdown("<div class='section-title'>📦 Export Results</div>",
                    unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.download_button("📄 JSON", exports["json"], file_name="audit.json")

        with col2:
            st.download_button("📝 Markdown", exports["markdown"], file_name="audit.md")

        with col3:
            st.download_button("📃 TXT", exports["txt"], file_name="audit.txt")

        with col4:
            st.download_button("🌐 HTML", exports["html"], file_name="audit.html")

