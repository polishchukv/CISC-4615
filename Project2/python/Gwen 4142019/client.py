import socket
import struct
import sys

text = "I love Fordham University in the New York City"
flag = 0
ack = 0
seq = 0
str = "NULL"

# window size is 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss = struct.pack("!50s3i",str.encode(),flag,ack,seq)
s.sendto(ss, ("127.0.0.1",1999))




'''

# flags
flag = 0
# acknowledgement numbers
ack = 0
# sequence numbers
seq = 0
# str of message initialize as NULL
str = "NULL"

# string we want to send
text = "I love Fordham University in the New York City"
# create an instance of Info()
var = Info()
# pickle and send
data_string = pickle.dumps(var)
# s = socket to connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send SYN
# AFTER receive SYN ack and seq no
    # send SYN ack and seq no and data

### to send data
# loop through string to send 1 char at a time
# increment and send ack and seq no
# receives ack

### to close connection
# send FIN
# receive ACK and FIN
# send ACK and close connection

# flag: SYN, ACK, FIN

# ss = struct.pack(data_string)

# ss = data we want to send
# ss = struct.pack("!50si",text.encode(),num)
# sends to server via s
s.sendto(ss,("127.0.0.1",1999))
s.sendto(data_string,("127.0.0.1",1999))
'''
