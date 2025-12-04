# ====================================================================
# NetDoc AI — AI Engine (GPT-powered Services)
# ====================================================================

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------
# CORE AI CALL
# --------------------
def ask_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are NetDoc AI — an expert network engineer, auditor and designer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]


# --------------------
# AI TROUBLESHOOTER
# --------------------
def ai_troubleshoot(config_text: str) -> str:
    prompt = f"""
Analyze the following network configuration and find:

1. Security misconfigurations
2. Routing issues
3. VLAN issues
4. Interface problems
5. Suggestions for optimization
6. Commands to fix the issues

CONFIG:
{config_text}
"""
    return ask_ai(prompt)


# --------------------
# AI NETWORK DESIGNER
# --------------------
def ai_design(requirements: str) -> str:
    prompt = f"""
You are a senior network architect.

Create a full network design including:

- High-level topology
- IP schema
- VLAN plan
- Routing design (OSPF/BGP)
- Firewall rules
- HA recommendations
- Hardware recommendations

REQUIREMENTS:
{requirements}
"""
    return ask_ai(prompt)


# --------------------
# AI LOG ANALYZER
# --------------------
def ai_log_analyzer(logs: str) -> str:
    prompt = f"""
You are a senior network SOC analyst.

Analyze these logs and return:

- What happened?
- Root cause
- Impact
- Threat severity
- Recommended mitigation actions

LOGS:
{logs}
"""
    return ask_ai(prompt)


# --------------------
# AI CONFIG COMMAND GENERATOR
# --------------------
def ai_generate_commands(request_text: str) -> str:
    prompt = f"""
Generate commands for:

- Cisco IOS
- Cisco Nexus
- Juniper JUNOS
- Fortinet FortiOS

Request:
{request_text}
"""
    return ask_ai(prompt)


# --------------------
# AI DOCUMENTATION BUILDER
# --------------------
def ai_document_config(config_text: str) -> str:
    prompt = f"""
Generate professional documentation for this configuration.

Include:

- Device summary
- Interfaces table
- VLANs
- Routing
- Security settings
- Best practices
- Recommendations

CONFIG:
{config_text}
"""
    return ask_ai(prompt)
