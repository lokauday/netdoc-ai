# ===============================================================
#  NetDoc AI — Export Engine (FINAL FIXED VERSION)
# ===============================================================

import json
import html

def export_all_formats(audit_result, topology):
    """
    FIXED: Accepts two arguments
        - audit_result (dict)
        - topology (mermaid string)
    Returns dictionary containing all export formats.
    """

    # JSON
    json_export = json.dumps(
        {
            "audit": audit_result,
            "topology": topology
        },
        indent=4
    )

    # MARKDOWN
    markdown_export = f"""
# NetDoc AI Audit Report

## 🔎 Security Audit
