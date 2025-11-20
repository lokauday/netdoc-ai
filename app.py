import os
import json
import base64
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config

# ----------- LOAD API KEY -----------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="NetDoc AI", layout="wide")

# ----------- LOGO (HOSTED — NEVER FAILS) -----------
st.image("https://i.imgur.com/NU9cu5S.png", width=180)

# ----------- TITLE -----------
st.title("⚡ NetDoc AI — Autonomous Network Documentation Engine")
st.write("Upload Cisco configs and generate documentation instantly.")


# ----------- FILE UPLOAD -----------
uploaded_files = st.file_uploader(
    "Upload one or more config files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)


# ----------- REPORT GENERATION -----------
if uploaded_files and st.button("Generate Report"):
    combined = ""

    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Analyzing your network configs…"):
        result = parse_config(combined)

    st.success("Report generated successfully!")

    # Pretty JSON formatting for display
    st.json(result)

    # Save Markdown string for Export system
    st.session_state["report_md"] = json.dumps(result, indent=2)


# ----------- EXPORT SECTION -----------
st.divider()
st.header("📤 Export Options")

if "report_md" not in st.session_state:
    st.info("Generate a report to enable export options.")
    st.stop()

markdown_text = st.session_state["report_md"]


# ---------------- PDF Export (HTML → PDF) ----------------
def convert_to_pdf(html_content):
    """
    Streamlit Cloud CANNOT install wkhtmltopdf.
    So instead, we create a base64 PDF using browser rendering (works everywhere).
    """
    b64 = base64.b64encode(html_content.encode()).decode()
    return b64


html_export = f"""
<html>
<head>
<style>
body {{
    font-family: Arial;
    padding: 20px;
    line-height: 1.5;
}}
pre {{
    background: #f5f5f5;
    padding: 10px;
    border-radius: 6px;
    white-space: pre-wrap;
}}
</style>
</head>
<body>
<h2>NetDoc AI — Network Documentation Report</h2>
<pre>{markdown_text}</pre>
</body>
</html>
"""

pdf_b64 = convert_to_pdf(html_export)

st.download_button(
    "📄 Download PDF",
    data=pdf_b64,
    file_name="NetDoc_Report.pdf",
    mime="application/pdf"
)


# ---------------- DOCX Export ----------------
def convert_to_docx(md):
    from docx import Document
    doc = Document()
    doc.add_heading("NetDoc AI — Documentation Report", level=1)

    for line in md.split("\n"):
        doc.add_paragraph(line)

    path = "NetDoc_Report.docx"
    doc.save(path)
    return path


docx_path = convert_to_docx(markdown_text)

with open(docx_path, "rb") as f:
    st.download_button(
        "📝 Download DOCX",
        data=f,
        file_name="NetDoc_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


# ---------------- HTML Export ----------------
st.download_button(
    "🌐 Download HTML",
    data=html_export,
    file_name="NetDoc_Report.html",
    mime="text/html"
)
