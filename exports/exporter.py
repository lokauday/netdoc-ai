# ===============================================================
#  NetDoc AI — Exporter (JSON / Markdown / HTML / TXT)
# ===============================================================

import json
from datetime import datetime


def export_all_formats(audit_result: dict, topology: str) -> dict:
    """
    Returns all export formats based on audit_result + topology.
    audit_result = dict
    topology = Mermaid topology string
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # JSON EXPORT
    json_export = json.dumps({
        "timestamp": timestamp,
        "audit": audit_result,
        "topology": topology
    }, indent=4)

    # MARKDOWN EXPORT
    markdown_export = f"""
# NetDoc AI — Audit Report
Generated: {timestamp}

## 🔍 Audit Result (JSON)
