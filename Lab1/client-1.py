from socket import *

serverName = 'localhost'

serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

clientMessage1 = 'Hello Fordham'

clientSocket.send(str.encode(clientMessage1))
#client sends message 1

serverResponse1 = clientSocket.recv(1024)
#client receives responsemessage1

print ('From Server: ', bytes.decode(serverResponse1))
#client prints responsemessage1

clientSocket.close()
#close socket
