import streamlit as st
from utils.parser import parse_config
from topology_engine import generate_topology_mermaid

# ===============================================================
#  PROFESSIONAL TOPOLOGY WORKSPACE
# ===============================================================

def topology_page():

    st.markdown("""
        <style>
            .panel {
                background: #23262d;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #343840;
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 14px;
            }
            .mermaid-box {
                background: #181a1f;
                padding: 18px;
                border-radius: 12px;
                border: 1px solid #2f3238;
                margin-top: 10px;
                overflow-x: auto;
            }
            textarea {
                font-family: monospace !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌐 Topology Generator")

    # --------------------------------------------------------
    #  TWO-COLUMN LAYOUT
    # --------------------------------------------------------
    left, right = st.columns([1, 2])

    # =======================
    # LEFT PANEL – CONFIG
    # =======================
    with left:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📄 Configuration Input</div>",
                    unsafe_allow_html=True)

        config_text = st.text_area(
            "Paste device configuration",
            height=350,
            placeholder="interface GigabitEthernet0/1\n switchport access vlan 10\n ..."
        )

        generate_btn = st.button("🚀 Generate Topology")

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # RIGHT PANEL – TOPOLOGY
    # =========================
    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🖥 Rendered Topology</div>",
                    unsafe_allow_html=True)

        if generate_btn:
            if not config_text.strip():
                st.warning("Please paste configuration first.")
            else:
                parsed = parse_config(config_text)
                topology = generate_topology_mermaid(parsed["raw"])

                st.markdown("<div class='mermaid-box'>", unsafe_allow_html=True)
                st.markdown(f"""
                ```mermaid
                {topology}
                ```
                """)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Paste a config and click **Generate Topology**.")

        st.markdown("</div>", unsafe_allow_html=True)

