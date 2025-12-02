# ===============================================================
#  NetDoc AI — Audit Engine
# ===============================================================

def run_security_audit(parsed):
    if isinstance(parsed, str):
        raw = parsed
    else:
        raw = parsed.get("raw", "")

    audit = {
        "line_count": raw.count("\n"),
        "contains_enable_secret": "enable secret" in raw.lower(),
        "contains_telnet": "telnet" in raw.lower(),
        "contains_http": "ip http server" in raw.lower(),
        "contains_https": "ip http secure-server" in raw.lower(),
    }

    return audit
