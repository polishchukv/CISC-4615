from socket import *

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('localhost',serverPort))

serverSocket.listen(1)

print ('The server is ready to receive')

while 1:
	connectionSocket, addr = serverSocket.accept()
	#connection established

	clientMessage1 = connectionSocket.recv(1024) 
	#receive clientmessage #1

	print(bytes.decode(clientMessage1))
	#print clientmessage #1, decoded in order to avoid the extra 'b' character

	serverResponse1 = 'Bye'

	connectionSocket.send(str.encode(serverResponse1))
	#server send response #1

	break

connectionSocket.close()
#close function outside the while loop
