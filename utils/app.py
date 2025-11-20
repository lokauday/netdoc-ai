import streamlit as st
from utils.parser import parse_config

st.set_page_config(page_title="NetDoc AI", layout="wide")

st.title("⚡ Network Documentation AI Agent")
st.write("Upload Cisco configs and generate documentation instantly.")

uploaded_files = st.file_uploader(
    "Upload one or more config files",
    type=["txt", "cfg", "log"],
    accept_multiple_files=True
)

if uploaded_files and st.button("Generate Report"):
    combined = ""
    for f in uploaded_files:
        combined += f"\n\n# FILE: {f.name}\n"
        combined += f.read().decode("utf-8")

    with st.spinner("Processing your configs..."):
        result = parse_config(combined)

    st.success("Report generated successfully!")
    st.json(result)
