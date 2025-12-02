# ===============================================================
#  NetDoc AI — SNMP Polling Engine
# ===============================================================

from pysnmp.hlapi import *
from database import SessionLocal, SNMPDevice, SNMPPoll


def snmp_get(ip, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication or errorStatus:
        return None

    for name, val in varBinds:
        try:
            return int(val)
        except:
            return str(val)

    return None


def poll_devices():
    db = SessionLocal()
    devices = db.query(SNMPDevice).all()

    for d in devices:
        cpu = snmp_get(d.ip_address, d.community, "1.3.6.1.4.1.9.2.1.57.0")
        memory = snmp_get(d.ip_address, d.community, "1.3.6.1.4.1.9.2.1.8.0")
        uptime = snmp_get(d.ip_address, d.community, "1.3.6.1.2.1.1.3.0")

        in_octets = snmp_get(d.ip_address, d.community, "1.3.6.1.2.1.2.2.1.10.1")
        out_octets = snmp_get(d.ip_address, d.community, "1.3.6.1.2.1.2.2.1.16.1")

        poll = SNMPPoll(
            device_id=d.id,
            cpu=cpu or 0,
            memory=memory or 0,
            uptime=uptime or 0,
            in_octets=in_octets or 0,
            out_octets=out_octets or 0,
        )

        db.add(poll)

    db.commit()
    db.close()
