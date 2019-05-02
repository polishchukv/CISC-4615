import socket
import sys
import struct

flag = 0
ack = 0
seq = 0
str = "NULL"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))

data, addr = s.recvfrom(1024)
str,flag,ack,seq = struct.unpack("!50s3i",data)
str = str.decode("utf-8").replace("\0","")
print("str:%s\nflag:%f\nack:%a\nseq:%s" % (str,flag,ack,seq))




'''
import socket
import sys
import struct
import pickle

# flags
flag = 0
# acknowledgement numbers
ack = 0
# sequence numbers
seq = 0
# char of message initialize as NULL
char = "NULL"

# create an isntance of Info()
var = Info()
# s = socket connection to client
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind to receive message
s.bind(("0.0.0.0", 1999))
# receives message from client
data,addr = s.recvfrom(1024)
data_variable = pickle.loads(data)
str = str + Info.char
# str,flag,ack,seq = struct.unpack("!50si",flag,ack,seq)
# str = str.decode("utf-8").replace("\0","")
print("str:%s\nnum:%d" % (str,seq))
'''
