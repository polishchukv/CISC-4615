import socket
import struct
import sys

#!50s2i50s
class TCP_struct:
	def __init__(self):
		self.Flag = 0
		self.Seq_Num = 0
		self.Ack_Num = 0
		self.Data = ""

sample = TCP_struct()
sample.Flag = "SYN"
sample.Seq_Num = 1
sample.Ack_Num = 0
sample.Data = "NULL"

#Client sends SYN
#Server sends SYN ACK
#Client sends ACK + Data

#!50s3i
#FLAG
#ACK
#SEQ
#CHAR

text = "Hello, World"
blank_text = "NULL"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))
num = 1

# Sending SYN
print("Sending SYN (num = 1)")
ss = struct.pack("!50si", blank_text.encode(), num)
s.sendto(ss, ("127.0.0.1", 1999))

while True:
	data, addr = s.recvfrom(1024)
	str, num = struct.unpack("!50si", data)
	str = str.decode("utf-8").replace("\0", "")

	if num == 2:
		# Sending ACK + Data
		print("\nReceived SYN ACK")
		print("str:%s\nnum:%d" % (str,num))

		print("\nSending ACK (num = 3)")
		num += 1
		ss = struct.pack("!50si", blank_text.encode(), num)
		s.sendto(ss, ("127.0.0.1", 1999))

		print("Sending Data (string)")
		break

	# Assuming all data has been sent, now need to go through finish sequence
