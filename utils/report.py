# utils/report.py

from typing import Dict, Any, List


def _get(d: Dict, key: str, default=""):
    value = d.get(key)
    return "" if value is None else value


def build_markdown_report(data: Dict[str, Any]) -> str:
    """
    Build a Markdown network documentation report from parsed JSON dict.
    """
    device = data.get("device_summary", {}) or {}
    vlans: List[Dict[str, Any]] = data.get("vlans", []) or []
    interfaces: List[Dict[str, Any]] = data.get("interfaces", []) or []
    neighbors: List[Dict[str, Any]] = data.get("neighbors", []) or []
    routing = data.get("routing_summary", {}) or {}
    ascii_topology = data.get("ascii_topology", "") or ""

    md = []

    md.append("# Network Documentation Report\n")

    # Device summary
    md.append("## Device Summary")
    md.append(f"- **Hostname:** {_get(device, 'hostname')}")
    md.append(f"- **Model:** {_get(device, 'model')}")
    md.append(f"- **Serial:** {_get(device, 'serial')}")
    md.append(f"- **OS Version:** {_get(device, 'os_version')}\n")

    # VLANs
    md.append("## VLANs")
    if vlans:
        md.append("| VLAN ID | Name | Ports |")
        md.append("|--------|------|-------|")
        for v in vlans:
            ports = ", ".join(v.get("ports", []) or [])
            md.append(f"| {_get(v, 'vlan_id')} | {_get(v, 'name')} | {ports} |")
    else:
        md.append("_No VLAN information found._")

    # Interfaces
    md.append("\n## Interfaces")
    if interfaces:
        md.append("| Interface | Description | IP Address | VLAN | Status | Protocol |")
        md.append("|-----------|-------------|-----------|------|--------|----------|")
        for intf in interfaces:
            md.append(
                f"| {_get(intf, 'name')} "
                f"| {_get(intf, 'description')} "
                f"| {_get(intf, 'ip_address')} "
                f"| {_get(intf, 'vlan')} "
                f"| {_get(intf, 'status')} "
                f"| {_get(intf, 'protocol')} |"
            )
    else:
        md.append("_No interface information found._")

    # Neighbors
    md.append("\n## Neighbors (CDP/LLDP)")
    if neighbors:
        md.append("| Local Interface | Neighbor Device | Neighbor Interface |")
        md.append("|----------------|-----------------|--------------------|")
        for n in neighbors:
            md.append(
                f"| {_get(n, 'local_interface')} "
                f"| {_get(n, 'neighbor_device')} "
                f"| {_get(n, 'neighbor_interface')} |"
            )
    else:
        md.append("_No neighbor information found._")

    # Routing summary
    md.append("\n## Routing Summary")
    dyn = routing.get("dynamic_protocols", []) or []
    md.append(f"- Dynamic Protocols: {', '.join(dyn)}")
    md.append(f"- Default Route: {_get(routing, 'default_route')}")
    md.append(f"- Total Routes: {_get(routing, 'total_routes')}")

    # ASCII topology
    md.append("\n## Topology (ASCII View)")
    if ascii_topology:
        md.append("```")
        md.append(ascii_topology)
        md.append("```")
    else:
        md.append("_No topology information generated._")

    return "\n".join(md)


def build_html_report(data: Dict[str, Any]) -> str:
    """
    Build a simple HTML network documentation report from parsed JSON dict.
    (No external libs needed.)
    """
    device = data.get("device_summary", {}) or {}
    vlans: List[Dict[str, Any]] = data.get("vlans", []) or []
    interfaces: List[Dict[str, Any]] = data.get("interfaces", []) or []
    neighbors: List[Dict[str, Any]] = data.get("neighbors", []) or []
    routing = data.get("routing_summary", {}) or {}
    ascii_topology = data.get("ascii_topology", "") or ""

    def esc(x):
        if x is None:
            return ""
        return str(x)

    html = []

    html.append("<html><head><meta charset='utf-8'><title>Network Documentation Report</title></head><body>")
    html.append("<h1>Network Documentation Report</h1>")

    # Device summary
    html.append("<h2>Device Summary</h2>")
    html.append("<ul>")
    html.append(f"<li><b>Hostname:</b> {esc(device.get('hostname'))}</li>")
    html.append(f"<li><b>Model:</b> {esc(device.get('model'))}</li>")
    html.append(f"<li><b>Serial:</b> {esc(device.get('serial'))}</li>")
    html.append(f"<li><b>OS Version:</b> {esc(device.get('os_version'))}</li>")
    html.append("</ul>")

    # VLANs
    html.append("<h2>VLANs</h2>")
    if vlans:
        html.append("<table border='1' cellspacing='0' cellpadding='4'>")
        html.append("<tr><th>VLAN ID</th><th>Name</th><th>Ports</th></tr>")
        for v in vlans:
            ports = ", ".join(v.get("ports", []) or [])
            html.append(
                f"<tr><td>{esc(v.get('vlan_id'))}</td>"
                f"<td>{esc(v.get('name'))}</td>"
                f"<td>{esc(ports)}</td></tr>"
            )
        html.append("</table>")
    else:
        html.append("<p><i>No VLAN information found.</i></p>")

    # Interfaces
    html.append("<h2>Interfaces</h2>")
    if interfaces:
        html.append("<table border='1' cellspacing='0' cellpadding='4'>")
        html.append("<tr><th>Interface</th><th>Description</th><th>IP Address</th><th>VLAN</th><th>Status</th><th>Protocol</th></tr>")
        for intf in interfaces:
            html.append(
                "<tr>"
                f"<td>{esc(intf.get('name'))}</td>"
                f"<td>{esc(intf.get('description'))}</td>"
                f"<td>{esc(intf.get('ip_address'))}</td>"
                f"<td>{esc(intf.get('vlan'))}</td>"
                f"<td>{esc(intf.get('status'))}</td>"
                f"<td>{esc(intf.get('protocol'))}</td>"
                "</tr>"
            )
        html.append("</table>")
    else:
        html.append("<p><i>No interface information found.</i></p>")

    # Neighbors
    html.append("<h2>Neighbors (CDP/LLDP)</h2>")
    if neighbors:
        html.append("<table border='1' cellspacing='0' cellpadding='4'>")
        html.append("<tr><th>Local Interface</th><th>Neighbor Device</th><th>Neighbor Interface</th></tr>")
        for n in neighbors:
            html.append(
                "<tr>"
                f"<td>{esc(n.get('local_interface'))}</td>"
                f"<td>{esc(n.get('neighbor_device'))}</td>"
                f"<td>{esc(n.get('neighbor_interface'))}</td>"
                "</tr>"
            )
        html.append("</table>")
    else:
        html.append("<p><i>No neighbor information found.</i></p>")

    # Routing summary
    html.append("<h2>Routing Summary</h2>")
    html.append("<ul>")
    dyn = routing.get("dynamic_protocols", []) or []
    html.append(f"<li><b>Dynamic Protocols:</b> {esc(', '.join(dyn))}</li>")
    html.append(f"<li><b>Default Route:</b> {esc(routing.get('default_route'))}</li>")
    html.append(f"<li><b>Total Routes:</b> {esc(routing.get('total_routes'))}</li>")
    html.append("</ul>")

    # ASCII topology
    html.append("<h2>Topology (ASCII View)</h2>")
    if ascii_topology:
        html.append("<pre>")
        html.append(esc(ascii_topology))
        html.append("</pre>")
    else:
        html.append("<p><i>No topology information generated.</i></p>")

    html.append("</body></html>")

    return "\n".join(html)
