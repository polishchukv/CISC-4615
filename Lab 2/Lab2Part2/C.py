import random
import socket
import operator
import sys
import binascii
import struct

def crc32(v):
	return binascii.crc32(v.encode())

if len(sys.argv) != 2:
	print("Usage: python " + sys.argv[0] + " <listen port>")
	sys.exit(-1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", int(sys.argv[1])))
print("Waiting..")

#C receives message and code
#C unpacks, checks that code is correct
#If code is correct, C prints "match"
#Parameters = 10000

while True:
	data, addr = s.recvfrom(1024) #receive struct data
	str, crc = struct.unpack("!50sL", data) #unpack struct data
	str = str.decode("utf-8").replace("\0", "") #decode str from bytes to string type

	if crc32(str) == crc:
		print("Match")
		if str == "bye":
			break
	else:
		print("Corrupt")
		if str[:-1] == "bye":
			break
