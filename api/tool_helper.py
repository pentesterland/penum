#!/usr/bin/env python3
from multiprocessing import Pool
import socket

def tool_port_map(tool):
    mapping = {"amass":30000,
               "subfinder":30001,
               "aiodnsbrute":30002,
               "sublist3r":30003,
               "gobuster":30004,
               "massdns":30005}
    return mapping[f"{tool}"]

def start_proc(tool, host, pool):
    return pool.apply_async(run_service, args=(tool, host))

def run_service(tool,host):
    """Run service and copy output from tool's container."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tool, tool_port_map(tool)))

    # Send host
    payload = bytes(f"{host}\n", encoding='utf-8')
    s.send(payload)

    output = b''
    while True:
        chunk = s.recv(2048)
        if b"DONE" in chunk:
            break
        elif chunk != b'':
            output += chunk

    # Store output on API host
    with open(f"/{tool}-{host}.out", "wb") as f:
        f.write(output)
    return
    #return str(output, encoding="utf-8").rstrip().split()

def get_output(tool,host):
    """Return the given tool's output as a list."""
    ret = ''
    try:
        output = b''
        with open(f"/{tool}-{host}.out", "rb") as f:
            output += f.read()
        ret = str(output, encoding="utf-8").rstrip().split()
    except FileNotFoundError as e:
        ret = f"Error: {e}..."
    return ret

def check_cache(host):
    """Checks if host has already been enumerated. Return boolean."""
    result = False
    # check if file names exists
    return result

def penum(host):
    """Main controller for tools"""
    pool = Pool()
    start_proc("subfinder", host, pool)
    start_proc("aiodnsbrute", host, pool)
    start_proc("amass", host, pool)
    return
