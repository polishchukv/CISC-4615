import socket
import struct
import sys
import binascii

#Parameters = 127.0.0.1 9000

def crc32(v):
     r = binascii.crc32(v.encode())
     return r

if len(sys.argv) != 3: #len check for arguments (from part1)
	print("Usage: python " + sys.argv[0] + " <ip> <listen port>")
	sys.exit(-1) #exit if wrong arguments

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creation of socket, no binding

while True:
	print("Input text:")
	text = sys.stdin.readline().strip() #all leading/trailing whitespaces removed from string
	ss = struct.pack("!50sL",text.encode(),crc32(text)) #struct pack function, denoted to encode w/ crc32
	s.sendto(ss,(sys.argv[1],int(sys.argv[2]))) #send ss (struct) instead of just text
	if text == "bye": #loop break
		break