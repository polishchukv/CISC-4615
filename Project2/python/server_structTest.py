import socket
import struct
import sys

class TCP_struct: # Contains the data, flag, sequence number, and acknowledgement number
	def __init__(self):
		self.Data = ""
		self.Flag = 0
		self.Seq_Num = 0
		self.Ack_Num = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))
print("Bound, waiting...\n")

outbound = TCP_struct()
inbound = TCP_struct()

while True:
	data, addr = s.recvfrom(1024)
	inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
	inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

	if inbound.Flag == 1: # Received SYN
		print("Received SYN")
		print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

		# Sending SYN ACK
		print("\nSending SYN ACK")
		outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num = inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num
		outbound.Flag += 1
		print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))
		
		ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
		s.sendto(ss, ("127.0.0.1", 2000))

	if inbound.Flag == 3: # Received ACK for SYN ACK, ready for data transfer
		print("\nReceived ACK for SYN ACK + Data")
		print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

	
	if inbound.Data == "Hello, World!":
		break