import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config
from docx import Document

# ------------ LOAD KEY ------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ------------ PAGE CONFIG ------------
st.set_page_config(page_title="NetDoc AI", layout="wide")

# ------------ LOGO ------------
st.image("https://i.imgur.com/NU9cu5S.png", width=180)

st.title("⚡ NetDoc AI — Autonomous Network Documentation Engine")
st.write("Upload configs → AI generates documentation instantly.")

# ------------ FILE UPLOAD ------------
uploaded_files = st.file_uploader(
    "Upload one or more config files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

# ------------ PROCESSING ------------
if uploaded_files and st.button("Generate Report"):
    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Processing your configs..."):
        result = parse_config(combined)

    st.success("Report generated!")
    st.json(result)

    st.session_state["report_json"] = result
    st.session_state["report_markdown"] = json.dumps(result, indent=2)

# ------------ EXPORT SECTION ------------
st.divider()
st.header("📤 Export Options")

if "report_markdown" not in st.session_state:
    st.info("Generate a report to enable export options.")
    st.stop()

markdown_text = st.session_state["report_markdown"]

# ----------------------- HTML EXPORT -----------------------
st.subheader("🌐 Export as HTML")

html_export = f"""
<html>
<head>
<title>NetDoc AI Report</title>
<style>
body {{
    font-family: Arial; 
    padding: 20px;
    max-width: 900px;
    margin: auto;
}}
pre {{
    background: #f4f4f4;
    padding: 15px;
    border-radius: 10px;
}}
</style>
</head>
<body>
<h1>NetDoc AI — Documentation Report</h1>
<pre>{markdown_text}</pre>
</body>
</html>
"""

st.download_button(
    "⬇️ Download HTML Report",
    data=html_export,
    file_name="NetDoc_Report.html",
    mime="text/html"
)

# ----------------------- DOCX EXPORT ------------------------
st.subheader("📄 Export as DOCX")

def generate_docx(text):
    doc = Document()
    doc.add_heading("NetDoc AI — Documentation Report", level=1)

    for line in text.split("\n"):
        doc.add_paragraph(line)

    # Save to memory
    from io import BytesIO
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

docx_file = generate_docx(markdown_text)

st.download_button(
    "⬇️ Download DOCX Report",
    data=docx_file,
    file_name="NetDoc_Report.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

# ----------------------- PDF EXPORT (Browser Print) ------------------------
st.subheader("🖨 Export as PDF")

st.info("PDF export works through browser print dialog (best quality).")

st.markdown("""
Click below to open the HTML version.  
Then press **Ctrl+P → Save as PDF**.
""")

st.download_button(
    "📄 Open HTML for PDF Printing",
    data=html_export,
    file_name="NetDoc_Report_for_PDF.html",
    mime="text/html"
)
