from socket import *
import sys
import os #import libraries
ack = "Ack"

class Server():
    def __init__(self,serverPort):#initialization
        self.serverPort = serverPort

    def create_socket(self):#socket creation
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', self.serverPort))
        print('The server  is ready to receive')
        return serverSocket
    
    def getFile(self,userInput,serverSocket,clientAddress):
        function, filename = userInput.split()#split input and filename
        if(os.path.isfile(filename)):#check if file is there
            serverSocket.sendto("found".encode(),clientAddress)#send found
            fh = open(filename, 'rb')#open in read mode
            msg = fh.read(4096)#read
            while(msg):
                finalMsg = msg
                ackMsgD = "xyz"
                while(ackMsgD != "Ack"):# send message and send till ack
                    serverSocket.sendto(finalMsg,clientAddress)
                    try:
                        ackMsg, clientAddress = serverSocket.recvfrom(1024)
                        ackMsgD = ackMsg.decode()
                    except:
                        print("Except")
                        continue
                msg = fh.read(2048)#read
            msg = "qazwsxed".encode()#end of file message
            finalMsg = msg
            serverSocket.sendto(finalMsg,clientAddress)#send
            ackMsg, clientAddress = serverSocket.recvfrom(1024)#ack receive
            fh.close()
        else:
            print("File not found")
            serverSocket.sendto("notfound".encode(),clientAddress)
            return
    
    def putFile(self,userInput,serverSocket):
        function, filename = userInput.split() #split user input
        fh = open(filename, 'wb+')#create and open a file with that filename
        clientMsg1 = None
        while(True):#get the file
            clientMsg, clientAddress = serverSocket.recvfrom(8192)
            serverSocket.sendto(ack.encode(), clientAddress)
            finalClientMsg = clientMsg
            try:
                if(finalClientMsg.decode() == "qazwsxed"):#check for end of file
                    fh.close()
                    return
            except:
                if (finalClientMsg == clientMsg1):#check for redundancy
                    continue
            fh.write(finalClientMsg)#write in file
            clientMsg1 = finalClientMsg#for the next packet
        fh.close()#close the file
        
    
    def renameFile(self,userInput,serverSocket,clientAddress):
        func, oldName, newName = userInput.split() #split for new and old filename
        try:#try if file is there and happens
            os.rename(oldName, newName)
            send = "Done!"
        except:#else wrong input
            send = "Wrong Input"
        ackMsgD = "xyz"
        while(ackMsgD != "Ack"):#ack message check
            serverSocket.sendto(send.encode(),clientAddress)#send if successful or unsuccessful
            try:
                ackMsg, clientAddress = serverSocket.recvfrom(1024)
                ackMsgD = ackMsg.decode()
            except:
                continue
        return
    
    def lst(self,userInput,serverSocket,clientAddress):
        onlyfiles = [f for f in os.listdir("./") if os.path.isfile(os.path.join("./", f))]#find only the files and not directories
        for file in onlyfiles:#split the list by spaces
            if(file.endswith(".py")):#check if ends with.py
                continue#if it does don send
            else: #send the file name and keep sending till ack
                ackMsgD = "xyz"
                while(ackMsgD != "Ack"):
                    serverSocket.sendto(file.encode(),clientAddress)
                    try:
                        ackMsg, clientAddress = serverSocket.recvfrom(1024)
                        ackMsgD = ackMsg.decode()
                    except:
                        continue
        msg = "qazwsxed".encode()#end of file msg
        serverSocket.sendto(msg,clientAddress)
    
    def ext(self,userInput,serverSocket,clientAddress):
        serverSocket.sendto("The server is now closed".encode(), clientAddress) #send closed
        serverSocket.close()#close the socket
        sys.exit()
        return

        
if __name__=='__main__':
    if int(sys.argv[1]) > 5000:#check if port greater than 5000
        arg = int(sys.argv[1])
        server = Server(arg)
        serverSocket = server.create_socket()#make socket
        while 1:#loop
            try:
                supermessage, clientAddress = serverSocket.recvfrom(2048)#recieve userinput
                message = supermessage.decode()#call appropriate function
                if message[:3] == "get":
                    server.getFile(message,serverSocket,clientAddress)
                elif message[:3] == "put":
                    server.putFile(message,serverSocket)
                elif message[:6] == "rename":
                    server.renameFile(message,serverSocket,clientAddress)
                elif message[:4] == "list":
                    server.lst(message,serverSocket,clientAddress)
                elif message[:4] == "exit":
                    server.ext(message,serverSocket,clientAddress)
                else:
                    continue
            except KeyboardInterrupt:
                print("Interrupted")
                sys.exit(0)
    else:
        exit(1)


