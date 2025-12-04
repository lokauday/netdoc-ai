# ============================================================
#  NetDoc AI — Core Engine (Audit + Topology + Export)
# ============================================================

from __future__ import annotations

from typing import Dict, List, Tuple
import io
import json
import zipfile

from utils.parser import parse_config, Device, Interface


# ------------------------------------------------------------
# SECURITY AUDIT
# ------------------------------------------------------------
def run_security_audit(config_text: str) -> Dict[str, object]:
    """
    Very lightweight static checks. You can extend this easily.
    """
    lines = config_text.splitlines()

    def has(pattern: str) -> bool:
        p = pattern.lower()
        return any(p in l.lower() for l in lines)

    audit: Dict[str, object] = {
        "line_count": len(lines),
        "contains_enable_secret": has("enable secret"),
        "contains_enable_password": has("enable password"),
        "contains_telnet": has("telnet"),
        "contains_http": has("ip http server"),
        "contains_https": has("ip http secure-server"),
        "contains_snmp": has("snmp-server"),
        "contains_acl": has("access-list"),
    }

    # quick “risk_score” (0–100) — purely illustrative
    penalties = 0
    if audit["contains_telnet"]:
        penalties += 30
    if audit["contains_http"]:
        penalties += 20
    if not audit["contains_https"]:
        penalties += 10
    if not audit["contains_enable_secret"] and audit["contains_enable_password"]:
        penalties += 15
    risk_score = max(0, min(100, penalties))
    audit["risk_score"] = risk_score

    return audit


# ------------------------------------------------------------
# TOPOLOGY (MERMAID)
# ------------------------------------------------------------

def _network_node_from_ip(ip: str) -> str:
    """
    Convert an IP into a coarse “network node” label.
    Example: 10.10.1.1 -> NET_10_10
    """
    try:
        octets = ip.split(".")
        return f"NET_{octets[0]}_{octets[1]}"
    except Exception:
        return "NET_MISC"


def generate_topology_mermaid(config_text: str) -> str:
    """
    Turn parsed devices into a Mermaid graph.
    """
    devices: List[Device] = parse_config(config_text)

    node_labels: Dict[str, str] = {}  # id -> label
    edges: List[Tuple[str, str]] = []

    # ----- build nodes & edges -----
    for dev in devices:
        dev_id = dev.hostname.replace("-", "_")
        node_labels[dev_id] = dev.hostname

        for intf in dev.interfaces:
            # Network node based on IP
            if intf.ip:
                net_id = _network_node_from_ip(intf.ip)
                node_labels.setdefault(net_id, net_id)
                edges.append((dev_id, net_id))

            # Neighbor-based link
            for n in intf.neighbors:
                neigh_id = n.replace("-", "_")
                # we don't know if neighbor exists as full device, but it is ok
                node_labels.setdefault(neigh_id, n)
                edges.append((dev_id, neigh_id))

    # If parsing failed and we have nothing, return simple stub
    if not node_labels:
        return "graph TD;\n    A[\"No topology information detected\"];"

    # ----- build Mermaid syntax -----
    lines: List[str] = ["graph TD;"]

    # nodes
    for node_id, label in node_labels.items():
        lines.append(f'    {node_id}["{label}"];')

    # edges
    for a, b in edges:
        lines.append(f"    {a} --> {b};")

    return "\n".join(lines)


# ------------------------------------------------------------
# EXPORT ENGINE (optional, but avoids ImportErrors)
# ------------------------------------------------------------

def export_all_formats(
    config_text: str, audit: Dict[str, object], topology: str
) -> bytes:
    """
    Create an in-memory ZIP with:
      - config.txt
      - audit.json
      - topology.mmd
    You can wire this to a Streamlit download button.
    """
    mem = io.BytesIO()

    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("config.txt", config_text)
        zf.writestr("audit.json", json.dumps(audit, indent=2))
        zf.writestr("topology.mmd", topology)

    mem.seek(0)
    return mem.getvalue()
