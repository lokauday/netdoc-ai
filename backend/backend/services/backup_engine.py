# ====================================================================
# NetDoc AI — Backup Engine (SSH pull)
# ====================================================================

from typing import Optional
from .ssh_engine import ssh_run_command


def get_running_config(ip: str, username: str, password: str) -> Optional[str]:
    """
    Fetch 'show running-config' via SSH
    """
    command = "show running-config"
    result = ssh_run_command(ip, username, password, command)
    return result
