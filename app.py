import streamlit as st
from utils.parser import parse_config
from utils.report import build_markdown_report, build_html_report

st.set_page_config(page_title="NetDoc AI", layout="wide")

st.title("⚡ Network Documentation AI Agent")
st.write("Upload Cisco configs (`show run`, `show vlan`, `show ip int brief`, `show cdp nei`, `show version`) and generate documentation.")


uploaded_files = st.file_uploader(
    "Upload one or more config files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True,
    help="You can export CLI output from switches/routers and upload them here."
)

if uploaded_files:
    if st.button("Generate Documentation Report"):
        # Combine all uploaded files into one big text blob
        combined = ""
        for f in uploaded_files:
            try:
                text = f.read().decode("utf-8", errors="ignore")
            except Exception:
                text = ""
            combined += f"\n\n# FILE: {f.name}\n"
            combined += text

        with st.spinner("Analyzing config and generating report..."):
            data = parse_config(combined)
            md_report = build_markdown_report(data)
            html_report = build_html_report(data)

        st.success("Report generated successfully!")

        # Show a preview of the Markdown report in the app
        st.subheader("📄 Report Preview (Markdown)")
        st.markdown(md_report)

        # Download buttons
        st.subheader("⬇️ Download Report Files")
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Markdown (.md)",
                data=md_report,
                file_name="netdoc_report.md",
                mime="text/markdown"
            )

        with col2:
            st.download_button(
                label="Download HTML (.html)",
                data=html_report,
                file_name="netdoc_report.html",
                mime="text/html"
            )

        st.info(
            "💡 Tip: Open the HTML file in a browser and use **Print → Save as PDF** "
            "to get a PDF version of the report."
        )
else:
    st.info("Upload at least one config file to get started.")
