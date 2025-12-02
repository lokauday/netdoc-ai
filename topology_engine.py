# ===============================================================
#  NetDoc AI — Topology Engine (Mermaid Generation)
#  FIXED: Works with raw config STRING (NOT dict)
# ===============================================================

def generate_topology_mermaid(raw_config: str):
    """
    Input is ALWAYS a raw config string.
    This version does NOT expect parsed['raw'] or parsed.get().
    """

    # Basic example topology extraction
    # (Replace with real CDP/LLDP/NDP parsing later)

    lines = raw_config.splitlines()

    connections = []
    hostname = "Device"

    # Try to extract hostname
    for line in lines:
        if line.lower().startswith("hostname"):
            hostname = line.split()[1]
            break

    # Try to extract simple neighbor patterns
    for line in lines:
        if "GigabitEthernet" in line and "connect" in line.lower():
            try:
                parts = line.split()
                local_int = parts[0]
                remote = parts[-1]
                connections.append((local_int, remote))
            except:
                pass

    # If nothing found, build a simple single-node graph
    if not connections:
        return f"""
flowchart TD
    {hostname}["{hostname}"]
"""

    # Build Mermaid diagram
    topo = "flowchart TD\n"

    for local, remote in connections:
        safe_local = local.replace("/", "_")
        safe_remote = remote.replace("/", "_")

        topo += f'    {safe_local}["{local}"] --> {safe_remote}["{remote}"]\n'

    return topo
