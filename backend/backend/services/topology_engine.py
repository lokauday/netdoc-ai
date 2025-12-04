# ====================================================================
# NetDoc AI — Topology Builder Engine (Mermaid v2)
# ====================================================================

from typing import Dict, List
from .parser import parse_config


def _network_node(ip: str) -> str:
    """Convert IP into a simple network node like NET_10_20"""
    parts = ip.split(".")
    if len(parts) >= 2:
        return f"NET_{parts[0]}_{parts[1]}"
    return "NET_UNKNOWN"


def generate_topology(config_text: str) -> str:
    parsed = parse_config(config_text)

    hostname = parsed["hostname"]
    interfaces = parsed["interfaces"]

    nodes = {hostname.replace("-", "_"): hostname}
    edges = []

    for intf in interfaces:
        if intf["ip"]:
            net = _network_node(intf["ip"])

            nodes.setdefault(net, net)
            edges.append((hostname, net))

        if intf["desc"]:
            # Basic detection of lowercase neighbor names
            desc = intf["desc"].replace(" ", "_")
            neighbor = desc.upper()

            if len(neighbor) <= 18:
                nodes.setdefault(neighbor, neighbor)
                edges.append((hostname, neighbor))

    # -------------------------------
    # MERMAID OUTPUT
    # -------------------------------
    out = ["graph TD;"]

    for node_id, label in nodes.items():
        out.append(f'    {node_id}["{label}"];')

    for a, b in edges:
        out.append(f"    {a.replace('-', '_')} --> {b.replace('-', '_')};")

    return "\n".join(out)
