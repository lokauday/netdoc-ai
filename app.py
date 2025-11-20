import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config
from docx import Document
import base64

# Load API Key
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="NetDoc AI", layout="wide")
st.title("⚡ NetDoc AI — Autonomous Network Documentation Engine")
st.write("Upload configs → AI creates documentation, auditing, topology & exports.")


# ------------------ AI HELPERS ------------------

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content


# ------------------ SECURITY AUDIT ------------------

def security_audit(config_text):
    prompt = f"""
You are a senior network security auditor.

Analyze the following network configuration and return a JSON with:
- insecure passwords
- missing ACLs
- VLAN leaks
- STP issues
- unused services
- risky configurations
- remediation steps

CONFIG:
{config_text}
"""

    result = ask_ai(prompt)
    return result


# ------------------ TOPOLOGY GENERATION ------------------

def generate_topology(config_text):
    prompt = f"""
Based on this config, generate ASCII network topology.

Use only:
[Device] --interface--> [Neighbor]

CONFIG:
{config_text}
"""

    return ask_ai(prompt)


# ------------------ EXPORT: DOCX ------------------

def export_docx(report_dict, topology, audit):
    doc = Document()
    doc.add_heading("NetDoc AI — Network Documentation Report", level=1)

    doc.add_heading("Device Summary", level=2)
    doc.add_paragraph(json.dumps(report_dict["device_summary"], indent=2))

    doc.add_heading("VLANs", level=2)
    doc.add_paragraph(json.dumps(report_dict["vlans"], indent=2))

    doc.add_heading("Interfaces", level=2)
    doc.add_paragraph(json.dumps(report_dict["interfaces"], indent=2))

    doc.add_heading("Neighbors", level=2)
    doc.add_paragraph(json.dumps(report_dict["neighbors"], indent=2))

    doc.add_heading("Routing", level=2)
    doc.add_paragraph(json.dumps(report_dict["routing_summary"], indent=2))

    doc.add_heading("AI-Generated Topology", level=2)
    doc.add_paragraph(topology)

    doc.add_heading("Security Audit", level=2)
    doc.add_paragraph(audit)

    # Save to bytes
    output = "NetDoc_Report.docx"
    doc.save(output)

    with open(output, "rb") as f:
        encoded = f.read()

    return encoded


# ------------------ EXPORT: HTML ------------------

def export_html(report_dict, topology, audit):
    html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
    <h1>NetDoc AI — Network Report</h1>

    <h2>Device Summary</h2>
    <pre>{json.dumps(report_dict["device_summary"], indent=2)}</pre>

    <h2>VLANs</h2>
    <pre>{json.dumps(report_dict["vlans"], indent=2)}</pre>

    <h2>Interfaces</h2>
    <pre>{json.dumps(report_dict["interfaces"], indent=2)}</pre>

    <h2>Neighbors</h2>
    <pre>{json.dumps(report_dict["neighbors"], indent=2)}</pre>

    <h2>Routing Summary</h2>
    <pre>{json.dumps(report_dict["routing_summary"], indent=2)}</pre>

    <h2>AI-Generated Topology</h2>
    <pre>{topology}</pre>

    <h2>AI-Generated Security Audit</h2>
    <pre>{audit}</pre>
    </body>
    </html>
    """

    return html.encode("utf-8")


# ------------------ MAIN ------------------

uploaded_files = st.file_uploader(
    "Upload configs (multiple allowed)",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

if st.button("Generate Documentation") and uploaded_files:
    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("AI analyzing configuration..."):
        report_dict = parse_config(combined)
        topology = generate_topology(combined)
        audit = security_audit(combined)

    st.success("Report generated!")
    st.json(report_dict)

    # DOCX
    docx_bytes = export_docx(report_dict, topology, audit)
    st.download_button(
        "📄 Download DOCX",
        data=docx_bytes,
        file_name="NetDoc_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # HTML
    html_bytes = export_html(report_dict, topology, audit)
    st.download_button(
        "🌐 Download HTML",
        data=html_bytes,
        file_name="NetDoc_Report.html",
        mime="text/html"
    )

    # PDF via browser print
    st.info("For PDF: Open HTML → Press CTRL+P → Save as PDF (100% reliable, zero errors).")
