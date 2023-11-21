
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
	print( "USAGE python " + sys.argv[0] + " <FILE NAME>" )

# Server address
serverAddr = str(sys.argv[1])

# Server port
serverPort = int(sys.argv[2])


# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = ""


def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	recvBuff = bytes(fileData, 'utf-8')
	
	# The temporary buffer
	tmpBuff = ""
	tmpBuff = bytes(fileData, 'utf-8')
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	return recvBuff


# Keep sending until all is sent
while True:

	inputCmd = input("ftp> ")

	if(inputCmd[0:3] == 'put'):

		fileName = inputCmd[4:]
		try:
			fileObj = open(fileName, "r")
		except:
			print("File does not exist.")
			# break
		
		numSent = 0

		fileDate = None

		while True:

			fileObj = open(fileName, "r")
			fileData = fileObj.read(65536)

			if fileData:
				dataSizeStr = str(len(fileData))

				while len(dataSizeStr) < 10:
					dataSizeStr = "0" + dataSizeStr

				fileData = dataSizeStr + fileData
				fileDateByt = bytes(fileData, 'utf-8')

				numSent = 0

				while len(fileData) > numSent:
					numSent += connSock.send(fileDateByt[numSent:])

			else:
				fileObj.close()
				# break

		print( "Sent ", numSent, " bytes." )

	elif(inputCmd[0:3] == 'get'):
		inputCmd = bytes(inputCmd, 'utf-8')
		connSock.send(inputCmd)
		fileData = ""
		recvBuff = ""
		fileSize = 0
		fileSizeBuff = ""
		fileSizeBuff = recvAll(connSock, 10)
		fileSize = int(fileSizeBuff)
		print( "The file size is ", fileSize )
		fileData = recvAll(connSock, fileSize)
		print( "The file data is: " )
		print( fileData )

	elif(inputCmd[0:3] == 'ls'):
		# command = 'ls'
		# command = bytes(command, 'utf-8')
		# connSock.send(command)
		# mySize = recvAll(connSock, 10)
		# sizeData = recvAll(connSock, int(mySize))
		# print(sizeData)

		command = 'ls'
		command = bytes(command, 'utf-8')
		connSock.send(command)

		recvBuff = ""
		fileSize = 0
		fileSizeBuff = ""
		fileSizeBuff = recvAll(connSock, 10)
		fileSize = int(fileSizeBuff)
		fileData = recvAll(connSock, fileSize)
		print(fileData)

	elif(inputCmd[0:4] == 'quit'):
		break
	
	# The file has been read. We are done
	else:
		print("Invalid command.")

	
# Close the socket and the file
connSock.close()
	
