import socket
import struct
import sys

text = "Hello, World!"
random = 4
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))
print("Bound, sending packages...")

i = 0
while i < len(text):
	package = text[i:i+4]
	print(package)
	print(type(package))
	ss = struct.pack("!4s1i", package.encode(), random)
	s.sendto(ss, ("127.0.0.1", 1999))
	
	i += 4

def send(s, temp): # Pack specified instance of TCP_struct and transmit to neighbor
	ss = struct.pack("!50s3i", temp.Data.encode(), temp.Flag, temp.Seq_Num, temp.Ack_Num)
	s.sendto(ss, ("127.0.0.1", 1999))

def receive(s, temp): # Receive transmission, decode, and return for reassignment outside scope
	data, addr = s.recvfrom(1024)
	temp = TCP_struct()
	temp.Data, temp.Flag, temp.Seq_Num, temp.Ack_Num = struct.unpack("!50s3i", data)
	temp.Data = temp.Data.decode("utf-8").replace("\0", "")
	return temp.Data, temp.Flag, temp.Seq_Num, temp.Ack_Num

def handshake(s, outbound, inbound): # Run and handle SYN and SYN ACK, then initiate SYN ACK ACK + data transfer
	print("Sending SYN")
	print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))
	send(s, outbound)

	while True:
		inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = receive(s, inbound)

		if inbound.Flag == 2: # Received SYN ACK
			print("\nReceived SYN ACK")
			print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))

			# Sending ACK for SYN ACK + data
			outbound.Flag += 1
			data_transfer(s, outbound, inbound)
			break

def data_transfer(s, outbound, inbound):
	print("\nSending ACK for SYN ACK")

	i = 0
	while i < len(text):
		outbound.Data = text[i:i+4]
		outbound.Seq_Num += 1
		print("Data: " + outbound.Data)
		print("Sequence Number: " + str(outbound.Seq_Num) + "\n")
		#print(type(package))
		send(s, outbound)
		
		i += 4