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
outbound.Flag = 1
outbound.Seq_Num = 0
outbound.Ack_Num = 0
outbound.Data = "NULL"
inbound = TCP_struct()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))
print("Bound, commencing handshake\n")

print("Sending SYN")
print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))
ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
s.sendto(ss, ("127.0.0.1", 1999))