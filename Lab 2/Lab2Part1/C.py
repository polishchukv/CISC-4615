import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python " + sys.argv[0] + " <liseten port>")
    sys.exit(-1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", int(sys.argv[1])))

print("Waiting..")
while True:
    data, addr = s.recvfrom(1024)
    print(data.decode("utf-8"))
    if data.decode("utf-8") == "bye":
        break