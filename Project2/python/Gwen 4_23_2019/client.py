# Gwendolyn Chu

'''
    Basic simulation of TCP protocol.
'''

import socket
import struct
import sys

# s = socket to receive from server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))

text = "I love Fordham University in the New York City"
flag = 0
ack = 0
seq = 0
str = "NULL"
windowBegin = 0
windowEnd = 3

# 1. send SYN
print ("Sending SYN")
ss = struct.pack("!i",flag)
s.sendto(ss,("127.0.0.1",1999))

# SYN-ACK
while True:
    data, addr = s.recvfrom(1024)
    flag, seq = struct.unpack("!2i", data)

    # 2. receive SYN-ACK
    if flag == 1:
        print("flag:%f\nseq:%s" % (flag, seq))
        print ("Received SYN-ACK")
        # according to picture on pg 2 of pdf
        ack = seq
        seq = flag

# send data
while ack < 10: # not if while True will work here
    print("Preparing ACK + data.")

    # 3. send characters in window
    for i in range (windowBegin, windowEnd):
        seq += 1
        ack += 1
        sendstr = text[i]
        print("Sending ACK + data.")
        ss = struct.pack("!1s2i",sendstr.encode(),seq,ack)
        s.sendto(ss,("127.0.0.1",1999))

    # slide window
    windowBegin = windowEnd + 1
    windowEnd = windowBegin + 4

    # 4. receive ack
    data, addr = s.recvfrom(1024)
    ack = struct.unpack("!2i", data)

# 5. sendFIN
flag = 0
ack = 0
print("Sending FIN")
ss = struct.pack("!i",flag)
s.sendto(ss,("127.0.0.1",1999))

#  6. receive FIN-ACK
while True:
    data, addr = s.recvfrom(1024)
    flag,ack = struct.unpack("!2i",data)

    if flag == 1 and ack == 1:
        ack += 1
        ss = struct.pack("!i",ack)
        s.sendto(ss,("127.0.0.1",1999))

s.close()
