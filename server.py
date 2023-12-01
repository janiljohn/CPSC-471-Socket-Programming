import socket
import subprocess

# The port on which to listen
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

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

def createFile(content):
    content = str(content, 'UTF-8')
    fileNameStartIdx = content.find("nameOfFile//") + 12
    fileNameEndIdx = content.find("//nameOfFile")
    fileName = content[fileNameStartIdx : fileNameEndIdx]
    fileName = fileName[fileName.rfind("/")+1:]

    try:
        f = open(fileName, "x")
    except:
        iter = 1
        while True:
            newFileName = fileName + " (" + str(iter) + ")"
            print(newFileName)
            try:
                f = open(newFileName, "x")
                break
            except:
                 iter += 1

    content = content[fileNameEndIdx+12:]
    f.write(content)
    f.close()

while True:
	
    print( "Waiting for connections..." )
		
	# Accept connections
    clientSock, addr = welcomeSock.accept()
	
    print( "Accepted connection from client: ", addr )
    print( "\n" )
	
    data = clientSock.recv(1024).decode()
	
    if(data[0:3] == 'put'):
        fileData = ""
        recvBuff = ""
        fileSize = 0
        fileSizeBuff = ""
		
        fileSizeBuff = recvAll(clientSock, 10)

        fileSize = int(fileSizeBuff)
		
        print ("The file size is ", fileSize)
		
        fileData = recvAll(clientSock, fileSize)

        print ("The file data is: ")
        createFile(fileData)
        print (fileData)
		
    elif(data[0:3] == 'get'):
		
        fileName = data[4:]

        try:
            fileObj = open(fileName, "r")
        except:
            print("File does not exist.")
            
        numSent = 0

        fileData = None

        while True:
            
            fileData = fileObj.read(65536)

            if fileData:
                dataSizeStr = str(len(fileData))

                while len(dataSizeStr) < 10:
                    dataSizeStr = "0" + dataSizeStr

                fileData = dataSizeStr + fileData

                numSent = 0

                while len(fileData) > numSent:
                    numSent += clientSock.send(fileData[numSent:].encode())

            else:
                fileObj.close()
                break

        print( "Sent ", numSent, " bytes." )

    elif(data[0:2] == 'ls'):
        # Run the command and capture the output
        result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Split the output into lines and iterate over them
            sendDate = ""
            fileData = ""
            dataSize = 0
            for line in result.stdout.split('\n'):
                sendDate = sendDate + str(line) + "\n"
            #get the size of this output
            dataSize = str(len(sendDate))
            #make that output's size to 10 bytes
            while len(dataSize) < 10:
                dataSize = "0" + dataSize

            #send it back to the client with the file size
            fileData = dataSize + sendDate
            fileDataByt = bytes(fileData, 'utf-8')

            numSent = 0

            while len(fileData) > numSent:
                 numSent += clientSock.send(fileDataByt[numSent:])
        else:
            print(f"Error: {result.returncode}")

    else:
        break

clientSock.close()

