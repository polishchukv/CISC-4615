from socket import *

serverName = 'localhost'

serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

clientMessage1 = 'Hello Fordham'
clientMessage2 = 'Hello CISC4615'
tempLog = [] #Logs all communications between server and client

clientSocket.send(str.encode(clientMessage1))
#client sends message 1

tempLog.append(clientMessage1)
#Log clientmessage1

serverResponse1 = clientSocket.recv(1024)
#client receives responsemessage1

tempLog.append(bytes.decode(serverResponse1))
#Log servermessage1

clientSocket.send(str.encode(clientMessage2))
#client sends message 2

tempLog.append(clientMessage2)
#Log clientmessage2

serverResponse2 = clientSocket.recv(1024)
#serve response w/ responsemessage2

tempLog.append(bytes.decode(serverResponse2))
#Log servermessage2

clientSocket.close()
#close connection

for x in tempLog:
	print (x)
#print all logged messages
