import socket
import struct
import sys

class TCP_struct:
	def __init__(self):
		self.Data = ""
		self.Flag = 0
		self.Seq_Num = 0
		self.Ack_Num = 0

outbound = TCP_struct()
inbound = TCP_struct()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))
print("Bound, waiting...\n")

data, addr = s.recvfrom(1024)
inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

if inbound.Flag == 1: # Received SYN
	print("Received SYN")
	print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))
