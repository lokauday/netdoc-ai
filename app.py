import os
import json
import streamlit as st
from openai import OpenAI
from utils.parser import parse_config

# ----------- LOAD API KEY FROM SECRETS OR LOCAL ENV -----------

api_key = None
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

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
