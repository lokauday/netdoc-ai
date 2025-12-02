# ===============================================================
#  NetDoc AI — Exporter (JSON / Markdown / HTML / TXT)
# ===============================================================

import json
from datetime import datetime


def export_all_formats(audit_result: dict, topology: str) -> dict:
    """
    Create all downloadable export formats.
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------
    # JSON EXPORT
    # -------------------------
    json_export = json.dumps({
        "timestamp": timestamp,
        "audit": audit_result,
        "topology": topology
    }, indent=4)

    # -------------------------
    # MARKDOWN EXPORT
    # IMPORTANT: Escape triple backticks inside f-string
    # -------------------------
    md_tick = "```"   # safe wrapper

    markdown_export = (
        "# NetDoc AI — Audit Report\n"
        f"Generated: {timestamp}\n\n"
        "## 🔍 Audit Result (JSON)\n"
        f"{md_tick}\n"
        f"{json.dumps(audit_result, indent=4)}\n"
        f"{md_tick}\n\n"
        "## 🌐 Topology (Mermaid)\n"
        f"{md_tick}mermaid\n"
        f"{topology}\n"
        f"{md_tick}\n"
    )

    # -------------------------
    # TEXT EXPORT
    # -------------------------
    text_export = (
        "NetDoc AI — Audit Report\n"
        f"Generated: {timestamp}\n\n"
        "AUDIT RESULT:\n"
        f"{json.dumps(audit_result, indent=4)}\n\n"
        "TOPOLOGY (Mermaid):\n"
        f"{topology}\n"
    )

    # -------------------------
    # HTML EXPORT
    # -------------------------
    html_export = f"""
<html>
<body style="font-family: Arial; padding: 20px;">
<h2>NetDoc AI — Audit Report</h2>
<p><strong>Generated:</strong> {timestamp}</p>

<h3>Audit Result</h3>
<pre>{json.dumps(audit_result, indent=4)}</pre>

<h3>Topology (Mermaid)</h3>
<pre>{topology}</pre>
</body>
</html>
"""

    return {
        "json": json_export,
        "markdown": markdown_export,
        "txt": text_export,
        "html": html_export,
    }
