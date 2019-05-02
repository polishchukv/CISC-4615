import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python " + sys.argv[0] + " <ip> <liseten port>")
    sys.exit(-1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    print("Input text:")
    text = sys.stdin.readline().strip()
    s.sendto(text.encode(),(sys.argv[1],int(sys.argv[2])))
    if text == "bye":
        break