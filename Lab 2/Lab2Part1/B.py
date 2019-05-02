import socket
import sys

if len(sys.argv) != 4:
    print("Usage: python " + sys.argv[0] + " <liseten port> <ip> <send port>")
    sys.exit(-1)

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind(("0.0.0.0", int(sys.argv[1])))

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Waiting..")
while True:
    data, addr = s1.recvfrom(1024)
    print(data.decode("utf-8"))
    s2.sendto(data,(sys.argv[2],int(sys.argv[3])))
    if data.decode("utf-8") == "bye":
        break