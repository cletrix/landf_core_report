import os
import uuid
import signal
import socket

import subprocess


def run_shell_command(command):
    result = subprocess.run(command,
                            shell=True,
                            capture_output=True,
                            text=True)
    print(f"{result.stdout.strip()}")


def generate_uppercase_uuid():
    uid = uuid.uuid4()
    uppercase_uid = str(uid).upper().replace("-", "")
    return uppercase_uid[:20]


def clear_terminal():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)
    return command


def clear_exit():
    signal.signal(signal.SIGINT, signal_handler)


def signal_handler(_, __):
    print('You pressed Ctrl+C! - Bye')
    os._exit(0)


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Não foi possível determinar o IP local: {e}")
        return None
