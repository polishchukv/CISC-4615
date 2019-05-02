from socket import *

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('localhost',serverPort))

serverSocket.listen(1)

print ('The server is ready to receive')

serverResponse1 = 'Hello CIS Students'
serverResponse2 = 'Bye'

while 1:
	connectionSocket, addr = serverSocket.accept()
	#connection established

	clientMessage1 = connectionSocket.recv(1024) 
	#receive clientmessage #1

	connectionSocket.send(str.encode(serverResponse1))
	#server send response #1

	clientMessage2 = connectionSocket.recv(1024)
	#receive clientmessage #2

	connectionSocket.send(str.encode(serverResponse2))
	#server sends response #2, encoded utf-8

	break

connectionSocket.close()
#close function outside the while loop
