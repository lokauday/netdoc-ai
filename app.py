import os
import json
import streamlit as st
from main import run_security_audit, generate_topology_mermaid, export_all_formats
from utils.parser import parse_config

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NetDoc AI — Datadog Dark Mode",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# GLOBAL CSS — Datadog Premium
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #1a1d21 !important;
}

div.block-container {
    padding-top: 2rem;
}

/* ----------------- NAV SIDEBAR ----------------- */
section[data-testid="stSidebar"] {
    background: #141619;
    border-right: 1px solid #2c2f35;
    padding-top: 24px;
}

.sidebar-title {
    font-size: 22px;
    color: #5b9bff;
    font-weight: 700;
    padding-bottom: 10px;
}

.sidebar-item {
    font-size: 17px;
    padding: 6px 0;
    color: #d7d7d7;
}

/* ----------------- TOP BANNER ----------------- */
.header-banner {
    background: linear-gradient(90deg, #22252b, #181a1e);
    padding: 20px 30px;
    border-radius: 10px;
    border: 1px solid #2e3238;
    box-shadow: 0 0px 10px rgba(0,0,0,0.4);
    margin-bottom: 25px;
}

.title-text {
    font-size: 30px;
    font-weight: 700;
    color: #5b9bff;
}

.sub-text {
    font-size: 15px;
    color: #c9c9c9;
}

/* ----------------- CONTENT CARDS ----------------- */
.card {
    background: #24272b;
    border-radius: 12px;
    padding: 22px;
    border: 1px solid #31363d;
    margin-bottom: 22px;
    box-shadow: 0 3px 20px rgba(0,0,0,0.35);
}

.card h3 {
    color: #8ab4ff;
    font-size: 22px;
    padding-bottom: 10px;
    border-bottom: 1px solid #333840;
}

.card p {
    color: #d1d1d1;
}


/* ----------------- MERMAID TOPOLOGY ----------------- */
.mermaid {
    background-color: #1f2125 !important;
    padding: 20px;
    border-radius: 10px;
}

/* ----------------- ABOUT PAGE IMAGE ----------------- */
.about-logo {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 220px;
    border-radius: 12px;
    box-shadow: 0 0 30px #5b9bff60;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>📂 Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Upload", "Documentation", "Security Audit", "Topology", "Exports", "About"]
    )

# -----------------------------
# TOP HEADER
# -----------------------------
st.markdown("""
<div class="header-banner">
    <div class="title-text">⚡ NetDoc AI — Datadog Dark Mode</div>
    <div class="sub-text">AI-powered network documentation engine with premium dark-mode interface.</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# PAGE 1 — UPLOAD
# =====================================================
if page == "Upload":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📁 Upload Configuration Files")

    uploaded_files = st.file_uploader(
        "Select config files:",
        type=["txt", "cfg", "log"],
        accept_multiple_files=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_files and st.button("Process Files"):
        combined = ""
        for f in uploaded_files:
            combined += f"\n\n# FILE: {f.name}\n"
            combined += f.read().decode("utf-8")

        with st.spinner("Analyzing configuration..."):
            result = parse_config(combined)

        st.session_state["report"] = result
        st.session_state["md"] = json.dumps(result, indent=2)

        st.success("✔ Configuration processed successfully!")


# =====================================================
# PAGE 2 — DOCUMENTATION
# =====================================================
elif page == "Documentation":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Generated Documentation")

    if "report" in st.session_state:
        st.json(st.session_state["report"])
    else:
        st.info("Upload configuration files first.")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PAGE 3 — SECURITY AUDIT
# =====================================================
elif page == "Security Audit":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🛡 Security Audit")

    if "report" not in st.session_state:
        st.info("Upload configuration files first.")
    else:
        audit = run_security_audit(st.session_state["report"])
        st.json(audit)

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PAGE 4 — TOPOLOGY
# =====================================================
elif page == "Topology":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌐 Network Topology Diagram")

    if "report" not in st.session_state:
        st.info("Upload configuration files first.")
    else:
        mermaid = generate_topology_mermaid(st.session_state["report"])
        st.markdown(f"```mermaid\n{mermaid}\n```")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PAGE 5 — EXPORTS
# =====================================================
elif page == "Exports":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📤 Export Options")

    if "md" not in st.session_state:
        st.info("Generate documentation first.")
    else:
        pdf, docx, html = export_all_formats(st.session_state["report"])

        st.download_button("📄 Download PDF", pdf, file_name="NetDoc_Report.pdf")
        st.download_button("📝 Download DOCX", docx, file_name="NetDoc_Report.docx")
        st.download_button("🌐 Download HTML", html, file_name="NetDoc_Report.html")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# PAGE 6 — ABOUT
# =====================================================
elif page == "About":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("###ℹ️ About NetDoc AI")

    st.write("AI-powered network documentation engine with premium Datadog dark-mode UI.")

    st.image("logo.png", width=240, output_format="PNG")

    st.markdown("</div>", unsafe_allow_html=True)
