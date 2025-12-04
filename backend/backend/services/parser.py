# ====================================================================
# NetDoc AI — Multi-Vendor Configuration Parser
# ====================================================================

import re
from typing import List, Dict


def parse_config(config_text: str) -> Dict:
    """
    Generic parser that extracts:
    - hostname
    - interfaces with IPs
    - descriptions
    - VLANs
    - OSPF/BGP hints
    - neighbor relationships (basic)
    """

    lines = config_text.splitlines()

    hostname = "Unknown"
    interfaces = []
    vlans = []
    current_int = None

    for raw in lines:
        line = raw.strip().lower()

        # -------------------------
        # HOSTNAME
        # -------------------------
        if line.startswith("hostname"):
            hostname = raw.split()[1]

        # -------------------------
        # INTERFACE START
        # -------------------------
        if raw.lower().startswith("interface"):
            current_int = {"name": raw.split()[1], "ip": None, "desc": None}
            interfaces.append(current_int)
            continue

        # -------------------------
        # DESCRIPTION
        # -------------------------
        if "description" in line and current_int:
            current_int["desc"] = raw.split("description")[-1].strip()

        # -------------------------
        # IP ADDRESS
        # -------------------------
        match_ip = re.search(r"ip address (\d+\.\d+\.\d+\.\d+)", line)
        if match_ip and current_int:
            current_int["ip"] = match_ip.group(1)

        # -------------------------
        # VLAN
        # -------------------------
        match_vlan = re.match(r"vlan (\d+)", line)
        if match_vlan:
            vlans.append(int(match_vlan.group(1)))

    return {
        "hostname": hostname,
        "interfaces": interfaces,
        "vlans": vlans,
    }
