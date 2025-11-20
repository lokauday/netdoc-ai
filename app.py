import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config

# ---------------- API KEY ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------- PDF (REPORTLAB) ----------------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

def generate_pdf(markdown_text):
    from io import BytesIO
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x = 40
    y = height - 40
    line_height = 14

    pdf.setFont("Helvetica", 10)

    for line in markdown_text.split("\n"):
        wrapped = simpleSplit(line, "Helvetica", 10, width - 80)
        for w in wrapped:
            if y < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 40
            pdf.drawString(x, y, w)
            y -= line_height

    pdf.save()
    buffer.seek(0)
    return buffer.read()


# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="NetDoc AI", layout="wide")

st.title("⚡ Network Documentation AI Agent")
st.write("Upload your switch/router configs and generate automated documentation.")

uploaded_files = st.file_uploader(
    "Upload 1 or more config files",
    type=["txt", "log", "cfg"],
    accept_multiple_files=True
)

if st.button("Generate Documentation") and uploaded_files:
    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Analyzing configuration..."):
        result = parse_config(combined)

    st.success("Report generated successfully!")
    st.json(result)

    md_report = json.dumps(result, indent=2)

    pdf_bytes = generate_pdf(md_report)

    st.download_button(
        "📥 Download PDF Report",
        data=pdf_bytes,
        file_name="Network_Documentation_Report.pdf",
        mime="application/pdf"
    )
