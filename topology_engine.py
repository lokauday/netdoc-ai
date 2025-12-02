# ===============================================================
#  NetDoc AI — Topology Generator
# ===============================================================

def generate_topology_mermaid(parsed):
    if isinstance(parsed, str):
        return "graph TD;\nA[Device] --> B[Neighbor];"

    neighbors = parsed.get("cdp_neighbors", {})

    mermaid = "graph TD;\n"

    for device, neigh_list in neighbors.items():
        for neigh in neigh_list:
            mermaid += f'    "{device}" --> "{neigh}";\n'

    return mermaid
