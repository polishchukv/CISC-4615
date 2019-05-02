import socket
import struct
import sys

text = ""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))
print("Bound, expecting packages")

while text != "Hello, World!":
#while True:
	data, addr = s.recvfrom(1024)
	inbound_text, random = struct.unpack("!4s1i", data)
	inbound_text = inbound_text.decode("utf-8").replace("\0", "")
	print("Received: " + inbound_text)
	print(type(inbound_text))

	text += inbound_text
	print("Current text: " + text)

def send(s, temp): # Pack specified instance of TCP_struct and transmit to neighbor
	ss = struct.pack("!50s3i", temp.Data.encode(), temp.Flag, temp.Seq_Num, temp.Ack_Num)
	s.sendto(ss, ("127.0.0.1", 2000))

def receive(s, temp): # Receive transmission, decode, and return for reassignment outside scope
	data, addr = s.recvfrom(1024)
	temp = TCP_struct()
	temp.Data, temp.Flag, temp.Seq_Num, temp.Ack_Num = struct.unpack("!50s3i", data)
	temp.Data = temp.Data.decode("utf-8").replace("\0", "")
	return temp.Data, temp.Flag, temp.Seq_Num, temp.Ack_Num

def handshake(s, outbound, inbound): # Run, receive SYN, send SYN ACK, then initiate wait for SYN ACK ACK + data transfer (separate function)
	while True:
		inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = receive(s, inbound)

		if inbound.Flag == 1: # Received SYN
			print("Received SYN")
			print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

			# Sending SYN ACK
			print("\nSending SYN ACK")
			outbound = inbound
			outbound.Flag += 1
			send(s, outbound)

		if inbound.Flag == 3: # Received ACK for SYN ACK, ready for data transfer
			print("\nReceived ACK for SYN ACK")
			print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

			# Should also receive data here - will add later
			break
