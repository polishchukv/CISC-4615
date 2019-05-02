import socket
import struct
import sys

# Flag Identifiers:
# 1 = SYN
# 2 = SYN ACK
# 3 = SYN ACK ACK + Data
# 4 = FIN
# 5 = FIN ACK
# 6 = FIN ACK ACK

# Contains the data, flag, sequence number, and acknowledgement number
class TCP_struct:
	def __init__(self):
		self.Data = ""
		self.Flag = 0
		self.Seq_Num = 0
		self.Ack_Num = 0

# For receiving/sending/handling packets
outbound = TCP_struct()
outbound.Flag = 1
outbound.Seq_Num = 0
outbound.Ack_Num = 0
outbound.Data = "NULL"
inbound = TCP_struct()

text = "I love Fordham University in the New York City."
i = 0

# Binds client.py to 2000 port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 2000))
print("Bound, commencing handshake\n")

# Sending SYN, Flag should be = 1
print("Sending SYN")
print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))

ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
s.sendto(ss, ("127.0.0.1", 1999))

# Receiving SYN ACK, decoding w/ proper format code: 50s = 50 character string, 3i = 3 integers
data, addr = s.recvfrom(1024)
inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")
if inbound.Flag == 2: # Received SYN ACK
	print("\nReceived SYN ACK")
	print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

# Sending SYN ACK ACK + beginning data transfer
outbound.Flag = inbound.Flag + 1 # Flag should now be 3
print("Outbound Flag: " + str(outbound.Flag))
print("\nSending ACK for SYN ACK + Data\n")

while i < len(text):
    outbound.Data = text[i:i+4] # 4 character window size
    outbound.Seq_Num += 1 # Up Seq_Num every time you send a window
    print("Sending Data: " + outbound.Data)
    print("Sending Sequence Number: " + str(outbound.Seq_Num))

    ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
    s.sendto(ss, ("127.0.0.1", 1999))

    # Expect acknowledgement
    data, addr = s.recvfrom(1024)
    inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
    inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

    if inbound.Ack_Num != outbound.Seq_Num:
        print("\nAcknowledgement and sequence number do not match:")
        print("Ack_Num: " + str(inbound.Ack_Num))
        print("Seq_Num: " + str(outbound.Seq_Num))
        break
    else:
        print("Received Acknowledgement Number: " + str(inbound.Ack_Num) + "\n")
        outbound.Ack_Num += 1

    i += 4 # No packet loss, shift window by 4 because all were successful

# End of data, send FIN
print("Sending FIN")
outbound.Flag += 1 # Flag should be 4 now
outbound.Data = "NULL"
outbound.Seq_Num = 0
outbound.Ack_Num = 0
print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))
ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
s.sendto(ss, ("127.0.0.1", 1999))

# Receive FIN ACK
data, addr = s.recvfrom(1024)
inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

if inbound.Flag == 5:
    print("\nReceived FIN ACK.")
    print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d\n" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

    print("Sending FIN ACK ACK.")
    outbound.Flag = inbound.Flag + 1
    print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))
    ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
    s.sendto(ss, ("127.0.0.1", 1999))

    s.close()
    print("\nConnection Closed!")
