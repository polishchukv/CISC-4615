# Gwendolyn Chu

'''
    Basic simulation of TCP protocol.
'''

import socket
import sys
import struct

# s = socket to receive fromt client
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))

flag = 0
ack = 0
seq = 0
str = "NULL"
mess = ""

# SYN
while True:
    # 1. receive SYN
    data,addr = s.recvfrom(1024)
    flag = struct.unpack("!i",data)
    while flag == 0:
        print("flag:%f" % (flag))
        # 2. send SYN-ACK
        print("\nPreparing SYN-ACK")
        flag += 1
        ss = struct.pack("!2i",flag,seq)
        s.sendto(ss,("127.0.0.1",2000))
        break

# receive data (no packet loss)
while ack < 10: # not if while True will work here
    # 3. received data message
    data, addr = s.recvfrom(1024)
    str,seq,ack = struct.unpack("!1s2i",data)
    str = str.decode("utf-8").replace("\0","")
    # add data to string
    mess += str
    print("\nReceived a DATA message")
    print("str:%s\nseq:%s\nack:%a" % (mess,seq,ack))
    # 4. send ack
    print("\nPreparing an ACK message")
    ack += 1
    ss = struct.pack("!i",ack)
    s.sendto(ss,("127.0.0.1",2000))

# reset values for FIN
ack = 0
flag = 0

# FIN
while True:
    # 5. receive FIN
    data, addr = s.recvfrom(1024)
    flag = struct.unpack("!i",data)

    if flag == 0:
        print("Received FIN")
        print("flag:%f" % (flag))
        # 6. send FIN-ACK
        print("Preparing FIN-ACK")
        flag += 1
        ack += 1
        ss = struct.pack("2i",flag,ack)
        s.sendto(ss,("127.0.0.1",2000))

    if ack == 2:
        s.close()
