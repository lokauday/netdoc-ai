# ====================================================================
# NetDoc AI — SNMP Monitoring Engine
# ====================================================================

from pysnmp.hlapi import *
from typing import Dict, Optional


def snmp_get(ip: str, community: str, oid: str) -> Optional[str]:
    """
    SNMP GET wrapper function
    """
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((ip, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    error_indication, error_status, error_index, var_binds = next(iterator)

    if error_indication or error_status:
        return None

    for var_bind in var_binds:
        return str(var_bind[1])

    return None


def poll_device(ip: str, community: str) -> Dict:
    """
    Poll basic system information
    """

    return {
        "sysName": snmp_get(ip, community, "1.3.6.1.2.1.1.5.0"),
        "sysDescr": snmp_get(ip, community, "1.3.6.1.2.1.1.1.0"),
        "uptime": snmp_get(ip, community, "1.3.6.1.2.1.1.3.0"),
        "cpu": snmp_get(ip, community, "1.3.6.1.4.1.9.2.1.57.0"),   # Cisco
        "memory": snmp_get(ip, community, "1.3.6.1.4.1.2021.4.6.0"), # UCD-SNMP
    }
