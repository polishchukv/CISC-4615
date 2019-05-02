import random
import socket
import operator
import sys
import binascii
import struct

def crc32(v):
	return binascii.crc32(v.encode())

if len(sys.argv) != 4:
	print("Usage: python " + sys.argv[0] + " <listen port> <ip> <send port>")
	sys.exit(-1)

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind(("0.0.0.0", int(sys.argv[1])))
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Waiting..")

#B receive message and code
#B follows 40% probability to change the message
#B forwards message to C
#Parameters = 9000 127.0.0.2 10000

while True:
	data, addr = s1.recvfrom(1024) #receive struct data
	str, crc = struct.unpack("!50sL", data) #unpack struct data
	str = str.decode("utf-8").replace("\0", "") #decode str from bytes to string type
	str_backup = str #backup str so that you can break loop even if it becomes modified

	if random.randint(0,100) < 40: #random num between 0-39 = 40% chance
		print("Altering Message...")
		str = str + "A" #add extra letter to string

	ss = struct.pack("!50sL", str.encode(), crc) #repack ss
	s2.sendto(ss, (sys.argv[2], int(sys.argv[3]))) #send to C.py
	
	if str_backup == "bye": #check original str 
		break