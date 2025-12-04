# ====================================================================
# NetDoc AI — Security Audit Engine v2
# ====================================================================

import re
from typing import Dict, List


def run_security_audit(config_text: str) -> Dict:
    lines = config_text.splitlines()

    def contains(pattern: str) -> bool:
        return any(pattern.lower() in l.lower() for l in lines)

    audit = {
        "total_lines": len(lines),
        "has_enable_secret": contains("enable secret"),
        "has_plaintext_passwords": contains("password 0"),
        "uses_telnet": contains("telnet"),
        "http_enabled": contains("ip http server"),
        "https_enabled": contains("ip http secure-server"),
        "snmp_public": contains("community public"),
        "snmp_private": contains("community private"),
        "weak_acl": contains("permit ip any any"),
        "missing_aaa": not contains("aaa new-model"),
    }

    # -------------------------------
    # RISK SCORE
    # -------------------------------
    score = 0

    if audit["uses_telnet"]:
        score += 25
    if audit["http_enabled"] and not audit["https_enabled"]:
        score += 15
    if audit["snmp_public"] or audit["snmp_private"]:
        score += 20
    if audit["weak_acl"]:
        score += 15
    if audit["missing_aaa"]:
        score += 10

    audit["risk_score"] = min(score, 100)

    # -------------------------------
    # RECOMMENDATIONS
    # -------------------------------
    rec = []
    if audit["uses_telnet"]:
        rec.append("Disable Telnet and enforce SSH")
    if audit["http_enabled"]:
        rec.append("Disable insecure HTTP server")
    if audit["snmp_public"]:
        rec.append("Replace SNMP community 'public'")
    if audit["weak_acl"]:
        rec.append("Avoid permit ip any any")

    audit["recommendations"] = rec

    return audit
