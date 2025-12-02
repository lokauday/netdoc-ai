# ===============================================================
#  NetDoc AI — Security Audit Engine
# ===============================================================

import json

# ---------------------------------------------------------------
# MAIN AUDIT FUNCTION
# ---------------------------------------------------------------
def run_security_audit(parsed_config: str):
    """
    parsed_config is now ALWAYS a plain string (raw config text).
    """

    raw = parsed_config  # <-- FIXED

    # Very simple demo audit – replace with your real logic
    audit = {
        "lines": raw.count("\n"),
        "contains_enable": "enable" in raw.lower(),
        "contains_password": "password" in raw.lower(),
        "raw_preview": raw[:200] + "..." if len(raw) > 200 else raw,
    }

    return audit
