# ====================================================================
# NetDoc AI — SSH Automation Engine
# ====================================================================

import paramiko
from typing import Optional


def ssh_run_command(ip: str, username: str, password: str, command: str) -> Optional[str]:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip, username=username, password=password, timeout=5)

        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()

        ssh.close()
        return result
    except Exception:
        return None
