# ============================================================
#  NetDoc AI — Config Parser (Cisco / Fortinet / Generic)
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict
import re


@dataclass
class Interface:
    name: str
    ip: Optional[str] = None
    description: Optional[str] = None
    neighbors: List[str] = field(default_factory=list)


@dataclass
class Device:
    hostname: str
    vendor: str = "generic"
    interfaces: List[Interface] = field(default_factory=list)


HOSTNAME_RE = re.compile(r"^hostname\s+(\S+)", re.IGNORECASE)
INT_RE = re.compile(r"^interface\s+(.+)", re.IGNORECASE)
IP_RE = re.compile(r"ip address\s+(\d+\.\d+\.\d+\.\d+)", re.IGNORECASE)
DESC_RE = re.compile(r"description\s+(.+)", re.IGNORECASE)

# Fortinet-style
FGT_EDIT_IF_RE = re.compile(r'^edit\s+"([^"]+)"')
FGT_SET_IP_RE = re.compile(r"set ip\s+(\d+\.\d+\.\d+\.\d+)")
FGT_SET_DESC_RE = re.compile(r"set alias\s+\"?(.+?)\"?$", re.IGNORECASE)


def _parse_cisco_device(lines: List[str]) -> Device:
    hostname = "DEVICE"
    interfaces: List[Interface] = []
    current_int: Optional[Interface] = None

    for raw in lines:
        line = raw.rstrip()

        m = HOSTNAME_RE.match(line.strip())
        if m:
            hostname = m.group(1)
            continue

        m = INT_RE.match(line.strip())
        if m:
            # start new interface
            current_int = Interface(name=m.group(1))
            interfaces.append(current_int)
            continue

        if current_int:
            m = DESC_RE.search(line)
            if m:
                current_int.description = m.group(1).strip()
                continue

            m = IP_RE.search(line)
            if m and not current_int.ip:
                current_int.ip = m.group(1).strip()
                continue

            # crude CDP/LLDP neighbor extraction if present in description
            # e.g. "to SW1 Gi1/0/1"
            if current_int.description:
                words = current_int.description.split()
                for w in words:
                    if w.isupper() and len(w) <= 10 and w != hostname:
                        if w not in current_int.neighbors:
                            current_int.neighbors.append(w)

    return Device(hostname=hostname, vendor="cisco", interfaces=interfaces)


def _parse_fortinet_device(lines: List[str]) -> Device:
    hostname = "FGT"
    interfaces: List[Interface] = []
    current_int: Optional[Interface] = None
    in_sys_global = False

    for raw in lines:
        line = raw.strip()

        if line.lower().startswith("config system global"):
            in_sys_global = True
            continue

        if in_sys_global and line.lower().startswith("set hostname"):
            parts = line.split()
            if len(parts) >= 3:
                hostname = parts[2].strip('"')
            continue

        if line.lower().startswith("config system interface"):
            # interface section coming up
            continue

        m = FGT_EDIT_IF_RE.match(line)
        if m:
            current_int = Interface(name=m.group(1))
            interfaces.append(current_int)
            continue

        if current_int:
            m = FGT_SET_IP_RE.search(line)
            if m and not current_int.ip:
                current_int.ip = m.group(1)
                continue

            m = FGT_SET_DESC_RE.search(line)
            if m:
                current_int.description = m.group(1).strip()
                continue

    return Device(hostname=hostname, vendor="fortinet", interfaces=interfaces)


def detect_vendor(config_text: str) -> str:
    text = config_text.lower()
    if "config system interface" in text or "fortigate" in text:
        return "fortinet"
    if "version" in text and "cisco ios" in text:
        return "cisco"
    if "hostname" in text and "interface" in text:
        return "cisco"
    return "generic"


def parse_config(config_text: str) -> List[Device]:
    """
    Parse raw configuration text into a list of Device objects.
    For now we treat the whole file as a single device, but we
    keep the list type to support multi-device files later.
    """
    lines = config_text.splitlines()
    vendor = detect_vendor(config_text)

    if vendor == "fortinet":
        dev = _parse_fortinet_device(lines)
    else:
        dev = _parse_cisco_device(lines)

    return [dev]


def summarize_devices(devices: List[Device]) -> List[Dict[str, object]]:
    """
    Small helper for debugging / JSON previews.
    """
    out: List[Dict[str, object]] = []
    for d in devices:
        out.append(
            {
                "hostname": d.hostname,
                "vendor": d.vendor,
                "interface_count": len(d.interfaces),
            }
        )
    return out
