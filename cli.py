import socket
import os
import sys
import subprocess

# Command line checks 
if len(sys.argv) < 2:
	print( "USAGE python " + sys.argv[0] + " <FILE NAME>" )

# Server address
serverAddr = str(sys.argv[1])

# Server port
serverPort = int(sys.argv[2])

# The number of bytes sent
numSent = 0

# The file data
fileData = ""

def restartConn():
	# Create a TCP socket
	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	connSock.connect((serverAddr, serverPort))

	return connSock


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

isInvalidArg = False

# Keep sending until all is sent
while True:

	if isInvalidArg == False:
		connSock = restartConn()

	inputCmd = input("ftp> ")

	if(inputCmd[0:3] == 'put'):
		isInvalidArg = False
		fileName = inputCmd[4:]
		validFile = True
		try:
			fileObj = open(fileName, "r")
		except:
			print("File does not exist.")
			validFile = False
			isInvalidArg = True

		if validFile:
			numSent = 0
			fileData = None

			connSock.send(bytes('put', 'utf-8'))

			addNameFlag = True
			fileData = "nameOfFile//" + fileName + "//nameOfFile"
			
			while True:

				if addNameFlag:
					fileData = fileData + fileObj.read(65536)
					addNameFlag = False
				else:
					fileData = fileObj.read(65536)

				if fileData:
					dataSizeStr = str(len(fileData))

					while len(dataSizeStr) < 10:
						dataSizeStr = "0" + dataSizeStr

					fileData = dataSizeStr + fileData
					fileDataByt = bytes(fileData, 'utf-8')

					numSent = 0

					while len(fileData) > numSent:
						numSent += connSock.send(fileDataByt[numSent:])

				else:
					fileObj.close()
					break

			print( "Sent ", numSent, " bytes." )

	elif(inputCmd[0:3] == 'get'):
		isInvalidArg = False
		validFile = True
		try:
			fileObj = open(inputCmd[4:], "r")
		except:
			print("File does not exist.")
			validFile = False
			isInvalidArg = True
		if validFile:
			inputCmd = bytes(inputCmd, 'utf-8')
			connSock.send(inputCmd)
			fileData = ""
			recvBuff = ""
			fileSize = 0
			fileSizeBuff = ""
			fileSizeBuff = recvAll(connSock, 10)
			fileSize = int(fileSizeBuff)
			print( "The file size is: ", fileSize )
			fileData = recvAll(connSock, fileSize)
			print( "The file data is: " )
			print(str(fileData, 'utf-8'))

	elif(inputCmd[0:2] == 'ls'):
		isInvalidArg = False
		command = 'ls'
		command = bytes(command, 'utf-8')
		connSock.send(command)

		recvBuff = ""
		fileData = ""
		fileSize = 0
		fileSizeBuff = ""
		fileSizeBuff = recvAll(connSock, 10)
		fileSize = int(fileSizeBuff)
		fileData = recvAll(connSock, fileSize)
		fileDataStr = fileData.decode('utf-8')
		print(fileDataStr)

	elif(inputCmd[0:4] == 'quit'):
		isInvalidArg = False
		break
	
	# The file has been read. We are done
	else:
		isInvalidArg = True
		print("Invalid command.")

	
# Close the socket and the file
connSock.close()