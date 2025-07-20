#!/bin/python3

import socket
import requests

def get_private_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        
        private_ip = s.getsockname()[0]
    except socket.error:
        private_ip = "127.0.0.1"
    finally:
        s.close()
    return private_ip

public_ip = requests.get("https://api.ipify.io").text
private_ip = get_private_ip()

print(f"Public IP: {public_ip}")
print(f"Private IP: {private_ip}")
