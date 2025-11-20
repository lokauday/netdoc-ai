import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config
from fpdf import FPDF

# ----------- LOAD API KEY FROM SECRETS OR LOCAL ENV -----------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ----------- PDF GENERATOR (FPDF – Works on Streamlit Cloud) -----------
def generate_pdf(markdown_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)

    for line in markdown_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin1")


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

    # Convert dict → markdown
    md_report = json.dumps(result, indent=2)

    # Generate PDF
    pdf_bytes = generate_pdf(md_report)

    st.download_button(
        "📥 Download PDF Report",
        data=pdf_bytes,
        file_name="Network_Documentation_Report.pdf",
        mime="application/pdf"
    )
