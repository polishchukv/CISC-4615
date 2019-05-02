import socket
import struct
import sys

class TCP_struct: # Contains the data, flag, sequence number, and acknowledgement number
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

text = "Hello, World!"
i = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))
print("Bound, commencing handshake\n")

print("Sending SYN")
print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))

ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
s.sendto(ss, ("127.0.0.1", 1999))

data, addr = s.recvfrom(1024)
inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

if inbound.Flag == 2: # Received SYN ACK
	print("\nReceived SYN ACK")
	print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

# Sending ACK for SYN ACK + data
outbound.Flag = inbound.Flag + 1
print("Outbound Flag: " + str(outbound.Flag))
print("\nSending ACK for SYN ACK + Data\n")

while i < len(text):
	outbound.Data = text[i:i+4]
	outbound.Seq_Num += 1
	print("Data: " + outbound.Data)
	print("Sequence Number: " + str(outbound.Seq_Num) + "\n")

	ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
	s.sendto(ss, ("127.0.0.1", 1999))

	i += 4