import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_MESSAGE = """
You are a senior network engineer and a strict JSON generator.
You ONLY output valid JSON. No text before or after, no comments, no explanations.
"""

def build_user_prompt(config_text: str) -> str:
    """
    Build the user prompt given the raw CLI text.
    """
    return f"""
You will be given raw CLI outputs from one or more Cisco switches/routers.

The text may contain (but is not limited to):
- show running-config
- show vlan brief
- show ip interface brief
- show cdp neighbors
- show lldp neighbors
- show version
- show ip route

From this, produce a SINGLE JSON object with the following exact structure:

{{
  "device_summary": {{
    "hostname": string or null,
    "model": string or null,
    "serial": string or null,
    "os_version": string or null
  }},
  "vlans": [
    {{
      "vlan_id": string,
      "name": string,
      "ports": [string, ...]
    }}
  ],
  "interfaces": [
    {{
      "name": string,
      "description": string or null,
      "ip_address": string or null,
      "vlan": string or null,
      "status": string or null,
      "protocol": string or null
    }}
  ],
  "neighbors": [
    {{
      "local_interface": string,
      "neighbor_device": string,
      "neighbor_interface": string
    }}
  ],
  "routing_summary": {{
    "dynamic_protocols": [string, ...],
    "default_route": string or null,
    "total_routes": int or null
  }},
  "ascii_topology": string
}}

Rules:
- All keys above MUST exist in the JSON you return.
- Use null if information is missing.
- Use empty lists [] if there are no items.
- Do NOT include any extra top-level keys.
- Do NOT include comments or explanations.
- Do NOT wrap JSON in markdown.
- Output MUST be valid JSON.

Here is the raw CLI text:

CONFIG_START
{config_text}
CONFIG_END
"""

def call_model(prompt: str) -> str:
    """
    Call OpenAI Chat Completions API and return the raw text response.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def extract_json(text: str) -> str:
    """
    If the model accidentally includes extra text, try to extract the JSON object
    by taking everything from the first '{' to the last '}'.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        # No JSON-looking content found
        raise ValueError(f"Model output did not contain a JSON object:\n{text}")
    return text[start : end + 1]

def parse_config(config_text: str) -> dict:
    """
    Main function to be called from app.py.
    Takes raw CLI text and returns a Python dict parsed from JSON.
    """
    user_prompt = build_user_prompt(config_text)
    raw = call_model(user_prompt)

    # First, try direct JSON parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract only the JSON portion
        json_str = extract_json(raw)
        return json.loads(json_str)

# Optional: allow quick testing from command line
if __name__ == "__main__":
    sample = """
show version
Cisco IOS Software, C2960X-UNIVERSALK9-M, Version 15.2(2)E7
System serial number: FOC1234X1CD

show vlan brief
10   USERS       active
20   SERVERS     active

show ip interface brief
Vlan10     10.0.10.1   up    up
Vlan20     10.0.20.1   up    up

show cdp neighbors
CORE1  Gig1/0/1   Gig0/1
"""
    data = parse_config(sample)
    print(json.dumps(data, indent=2))
