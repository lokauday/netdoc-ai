# ===============================================================
#  NetDoc AI — Export Engine (Fixed)
# ===============================================================

import json
import html

def export_all_formats(audit_result, topology):
    """
    Takes:
        audit_result (dict)
        topology (mermaid string)

    Returns:
        dict with json, markdown, txt, html versions
    """

    # JSON Export
    json_export = json.dumps({
        "audit": audit_result,
        "topology": topology
    }, indent=4)

    # Markdown Export
    markdown = (
        "# NetDoc AI Audit Report\n\n"
        "## Security Audit\n"
        f"```\n{json.dumps(audit_result, indent=4)}\n```\n\n"
        "## Topology\n"
        f"```mermaid\n{topology}\n```\n"
    )

    # TXT Export
    txt_export = (
        "=== NetDoc AI Audit Report ===\n\n"
        "=== Security Audit ===\n"
        f"{json.dumps(audit_result, indent=4)}\n\n"
        "=== Topology (Mermaid) ===\n"
        f"{topology}\n"
    )

    # HTML Export
    html_export = f"""
    <html>
    <body style="font-family: Arial; padding: 20px; background: #f7f7f7;">
        <h1>NetDoc AI Audit Report</h1>

        <h2>Security Audit</h2>
        <pre>{html.escape(json.dumps(audit_result, indent=4))}</pre>

        <h2>Topology</h2>
        <pre>{html.escape(topology)}</pre>
    </body>
    </html>
    """

    return {
        "json": json_export,
        "markdown": markdown,
        "txt": txt_export,
        "html": html_export
    }
