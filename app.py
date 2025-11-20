import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config
from docx import Document
from docx.shared import Inches

# ---------------------------------------------------------
# LOAD API KEY
# ---------------------------------------------------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------------------------------------------------
# PAGE CONFIG + LOGO
# ---------------------------------------------------------
st.set_page_config(page_title="NetDoc AI", layout="wide")

st.image("https://i.imgur.com/NU9cu5S.png", width=180)

st.title("⚡ NetDoc AI — Autonomous Network Documentation Engine")
st.write("Upload Cisco configs and generate documentation instantly.")

# ---------------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload one or more config files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

# ---------------------------------------------------------
# DOCX GENERATOR
# ---------------------------------------------------------
def generate_docx(report_dict):
    doc = Document()

    # Add Logo
    doc.add_picture("logo.png", width=Inches(1.8))
    doc.add_heading("NetDoc AI — Network Documentation Report", level=1)

    # Write key-value sections
    doc.add_heading("1. Device Summary", level=2)
    for k, v in report_dict.get("device_summary", {}).items():
        doc.add_paragraph(f"{k}: {v}")

    doc.add_heading("2. VLANs", level=2)
    for vlan in report_dict.get("vlans", []):
        doc.add_paragraph(json.dumps(vlan, indent=2))

    doc.add_heading("3. Interfaces", level=2)
    for iface in report_dict.get("interfaces", []):
        doc.add_paragraph(json.dumps(iface, indent=2))

    doc.add_heading("4. Neighbors", level=2)
    for nei in report_dict.get("neighbors", []):
        doc.add_paragraph(json.dumps(nei, indent=2))

    doc.add_heading("5. Routing Summary", level=2)
    doc.add_paragraph(json.dumps(report_dict.get("routing_summary", {}), indent=2))

    doc.add_heading("6. Topology (ASCII)", level=2)
    doc.add_paragraph(report_dict.get("ascii_topology", ""))

    # Save to bytes
    from io import BytesIO
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()


# ---------------------------------------------------------
# PROCESS CONFIGS
# ---------------------------------------------------------
if uploaded_files and st.button("Generate Report"):
    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Processing your configs..."):
        result = parse_config(combined)

    st.success("Report generated!")
    st.json(result)

    # Save for export features
    st.session_state["report_data"] = result

# ---------------------------------------------------------
# EXPORT SECTION
# ---------------------------------------------------------
st.divider()
st.header("📤 Export Options")

if "report_data" in st.session_state:

    # DOCX EXPORT BUTTON
    docx_bytes = generate_docx(st.session_state["report_data"])

    st.download_button(
        "📄 Download DOCX Report",
        data=docx_bytes,
        file_name="NetDoc_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

else:
    st.info("Generate a report to enable export options.")
