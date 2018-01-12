from socket import *
import sys
import os #import required libraries
ack = "Ack"

class Client():
    def __init__(self,serverName,serverPort,serverIP):  #init function
        try:
            self.serverName = serverName
            self.serverPort = serverPort
            self.serverIP = serverIP
        except: #if the socket doesnt get created
            print("Socket creation failed")
            exit(1)
        
    def create_socket(self):  #socket creation
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.connect((self.serverIP,self.serverPort))
        return clientSocket
    
    def getFile(self,userInput,clientSocket):
        function, filename = userInput.split() #breaks userinput based on spaces
        clientSocket.sendto(userInput.encode(),(self.serverName,self.serverPort))  #sending userinput
        Msg, serverAddress = clientSocket.recvfrom(1024) #message recieved from the server
        msg = Msg.decode()
        if(Msg.decode() == "found"):  #checks the message if it is found or not found
            fileName = "recieved_" + filename #changing filename
            fh = open(fileName, 'wb+') #opens and creates a new file with filename 
            serverMsg1 = None #initialization
            while(True):  
                serverMsg, serverAddress = clientSocket.recvfrom(8196)
                clientSocket.sendto(ack.encode(), (self.serverName,self.serverPort))
                finalServerMsg = serverMsg   #recieveing the data in blocks
                try:
                    if(finalServerMsg.decode() == "qazwsxed"): #checking if EOF(end of files) in my case sppeciefied by qazwsxed
                        fh.close() #close the file
                        print("File recieved")
                        return
                except:
                    if (finalServerMsg == serverMsg1): #checking if packet loss
                        continue
                    fh.write(finalServerMsg) #write message in file
                    serverMsg1 = finalServerMsg #for checking for the next packet
            fh.close()
        else: #if file not found
            print("File not found")
            return
            
    
    def putFile(self,userInput,clientSocket):
        function, filename = userInput.split()
        if(os.path.isfile(filename)):  #checks if file is present in the directory
            clientSocket.sendto(userInput.encode(),(self.serverName,self.serverPort)) #send user input
            print ("Sending file")
            fh = open(filename, 'rb') #open file in read mode
            msg = fh.read(2048) #read
            while(msg):
                finalMsg = msg
                ackMsgD = "xyz"
                while(ackMsgD != "Ack"): #looping for reliability
                    clientSocket.sendto(finalMsg,(self.serverName,self.serverPort)) #send the read message
                    try:
                        ackMsg, serverAddress = clientSocket.recvfrom(1024) #try if you got ack msg
                        ackMsgD = ackMsg.decode()
                    except:
                        continue
                msg = fh.read(2048)
            msg = "qazwsxed".encode() #end of file
            finalMsg = msg
            clientSocket.sendto(finalMsg,(self.serverName,self.serverPort)) #send the end of file
            ackMsg, serverAddress = clientSocket.recvfrom(1024) #ack recieveing
            fh.close() #close file
            print("Sent")
        else:
            print ("File not found")
            return
    
    def renameFile(self,userInput,clientSocket):
        clientSocket.sendto(userInput.encode(),(self.serverName,self.serverPort))#send user input
        serverMsg, serverAddress = clientSocket.recvfrom(1024)#recieve message if done or not
        Msg = serverMsg.decode()
        clientSocket.sendto(ack.encode(),(self.serverName,self.serverPort))#send ack
        print("Done!")
        return
    
    def lst(self,userInput,clientSocket):
        clientSocket.sendto(userInput.encode(),(self.serverName,self.serverPort)) #send user input
        serverMsg1 = None
        i = 1
        while(i): #loop for files recieving
            serverMsg, serverAddress = clientSocket.recvfrom(8192) #recieve filename
            clientSocket.sendto(ack.encode(), (self.serverName,self.serverPort))#send ack
            file = serverMsg.decode()
            if (file == "qazwsxed"):#check if end
                return
            if (file == serverMsg1): #check if redundent
                clientSocket.sendto(ack.encode(), (self.serverName,self.serverPort))
                continue
            serverMsg1 = file
            i = i + 1
            print(file)#print filename
    
    def ext(self,userInput,clientSocket):
        clientSocket.sendto(userInput.encode(),(self.serverName,self.serverPort))#send command
        serverMsg, serverAddress = clientSocket.recvfrom(2048)#wait for server to close
        msg = serverMsg.decode()
        print(msg)
        clientSocket.close()#close the client
        sys.exit()
    
    def Els(self,userInput):
        print("Command not understood")
        

if __name__=='__main__':
    client=Client("localhost",int(sys.argv[2]),sys.argv[1])#make socket
    clientSocket = client.create_socket()
    userInput = "NULL"
    while(userInput != "exit"): #loop for user input
        print("1:get[file_name] \n2:put[file_name] \n3:rename[old_file_name][new_file_name] \n4:list \n5:exit")
        userInput = input("Please enter the command:")
        if userInput[:3] == "get":
            client.getFile(userInput, clientSocket)
        elif userInput[:3] == "put":
            client.putFile(userInput, clientSocket)
        elif userInput[:6] == "rename":
            client.renameFile(userInput, clientSocket)
        elif userInput[:] == "list":
            client.lst(userInput, clientSocket)
        elif userInput[:] == "exit":
            client.ext(userInput, clientSocket)
        else:
            client.Els(userInput)
    exit(1)
    

