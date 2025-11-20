import os
import json
import textwrap
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config
from fpdf import FPDF

# ---------------- API KEY HANDLING ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------- PDF GENERATOR ----------------
def generate_pdf(markdown_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    safe_text = markdown_text.replace("\t", "    ")

    for line in safe_text.split("\n"):
        # wrap lines safely
        wrapped_lines = textwrap.wrap(line, width=90)

        if not wrapped_lines:
            pdf.ln(5)  # blank line
        else:
            for w in wrapped_lines:
                # replace characters that break FPDF
                safe = w.replace("•", "-").replace("→", "->").replace("—", "-")
                pdf.multi_cell(0, 5, safe)

    return pdf.output(dest="S").encode("latin-1")


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="NetDoc AI", layout="wide")
st.title("⚡ Network Documentation AI Agent")
st.write("Upload your configs → get JSON + PDF report instantly.")

uploaded_files = st.file_uploader(
    "Upload configuration files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

if st.button("Generate Documentation") and uploaded_files:
    combined = ""

    for f in uploaded_files:
        combined += f"\n\n# FILE: " + f.name + "\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Analyzing configuration..."):
        parsed = parse_config(combined)

    st.success("Report generated!")
    st.json(parsed)

    # -------- BUILD CLEAN MARKDOWN REPORT ----------
    md = "# Network Documentation Report\n\n"

    # device summary
    dev = parsed.get("device_summary", {})
    md += "## Device Summary\n"
    md += f"- Hostname: {dev.get('hostname')}\n"
    md += f"- Model: {dev.get('model')}\n"
    md += f"- Serial: {dev.get('serial')}\n"
    md += f"- OS Version: {dev.get('os_version')}\n\n"

    # VLANs
    md += "## VLANs\n"
    for v in parsed.get("vlans", []):
        md += f"- VLAN {v.get('vlan_id')} — {v.get('name')}\n"
    md += "\n"

    # Interfaces
    md += "## Interfaces\n"
    for i in parsed.get("interfaces", []):
        md += f"- {i.get('name')} — {i.get('ip_address')} ({i.get('status')})\n"
    md += "\n"

    # Neighbors
    md += "## Neighbors\n"
    for n in parsed.get("neighbors", []):
        md += f"- {n.get('local_interface')} ↔ {n.get('neighbor_device')} ({n.get('neighbor_interface')})\n"
    md += "\n"

    # Routing
    md += "## Routing Summary\n"
    r = parsed.get("routing_summary", {})
    md += f"- Protocols: {r.get('dynamic_protocols')}\n"
    md += f"- Default Route: {r.get('default_route')}\n"
    md += f"- Total Routes: {r.get('total_routes')}\n\n"

    # ASCII Topology
    md += "## Topology\n"
    topo = parsed.get("ascii_topology", "")
    md += topo + "\n\n"

    # ---- GENERATE SAFE PDF ----
    pdf_bytes = generate_pdf(md)

    st.download_button(
        "📥 Download PDF Report",
        data=pdf_bytes,
        file_name="Network_Documentation_Report.pdf",
        mime="application/pdf"
    )
