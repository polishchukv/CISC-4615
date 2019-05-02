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

# Binds server.py to 1999 port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 1999))
print("Bound, waiting...\n")

# For receiving/sending/handling packets and only acknowledging SYN ACK ACK once
outbound = TCP_struct()
inbound = TCP_struct()
acknowledge_3 = False
text = ""

# While true - waiting for incoming messages
while True:
    # !50s3i refers to pack format: 50 char string + 3 ints
    data, addr = s.recvfrom(1024)
    inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num = struct.unpack("!50s3i", data)
    inbound.Data = inbound.Data.decode("utf-8").replace("\0", "")

    # Received SYN
    if inbound.Flag == 1:
        print("Received SYN")
        print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

        # Sending SYN ACK in response to SYN
        print("\nSending SYN ACK")
        outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num = inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num
        outbound.Flag = inbound.Flag + 1 # Outbound Flag should now be 2
        print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))

        ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
        s.sendto(ss, ("127.0.0.1", 2000))

    # Received SYN ACK ACK, ready for data transfer
    if inbound.Flag == 3:
        if acknowledge_3 == False:
            print("\nReceived ACK for SYN ACK + Data")
            acknowledge_3 = True

        print("\nReceived New Data:")
        print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))
        text += inbound.Data

        # Send back acknowledgement
        outbound.Data = inbound.Data
        outbound.Flag = inbound.Flag
        outbound.Seq_Num = inbound.Seq_Num
        outbound.Ack_Num = inbound.Seq_Num
        ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
        s.sendto(ss, ("127.0.0.1", 2000))

    if inbound.Flag == 4:
        print("\nReceived FIN.")
        print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d\n" % (inbound.Data, inbound.Flag, inbound.Seq_Num, inbound.Ack_Num))

        print("Sending FIN ACK.")
        outbound.Data = inbound.Data
        outbound.Flag = inbound.Flag + 1
        outbound.Seq_Num = inbound.Seq_Num
        outbound.Ack_Num = inbound.Ack_Num
        print("Data: %s\nFlag: %d\nSequence Number: %d\nAcknowledgement Number: %d" % (outbound.Data, outbound.Flag, outbound.Seq_Num, outbound.Ack_Num))

        ss = struct.pack("!50s3i", outbound.Data.encode(), outbound.Flag, outbound.Seq_Num, outbound.Ack_Num)
        s.sendto(ss, ("127.0.0.1", 2000))

    if inbound.Flag == 6:
        print("\nReceived FIN ACK ACK.")
        print("Final Message: " + text)
        print("\nConnection closed!")
        s.close()
        break
