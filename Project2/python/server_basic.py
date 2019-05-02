import socket
import sys
import struct

blank_text = "NULL"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))

while True:
	data, addr = s.recvfrom(1024)
	str, num = struct.unpack("!50si", data)
	str = str.decode("utf-8").replace("\0", "")

	if num == 1:
		# Receiving SYN, then sending SYN ACK
		print("Received SYN")
		print("str:%s\nnum:%d" % (str,num))
		print("\nSending SYN ACK (num = 1)")
		num += 1
		ss = struct.pack("!50si", blank_text.encode(), num)
		s.sendto(ss, ("127.0.0.1", 2000))

	if num == 3:
		# Receiving ACK, then beginning data reception/acknowledgement
		print("\nReceiving ACK")
		print("str:%s\nnum:%d" % (str,num))

		print("Receiving Data")

		break

	# Server doesn't know when the data stream is done, so client will have to initialize finish seq