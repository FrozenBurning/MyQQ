import socket

class ConnectionTool:
    def __init__(self):
        self.ServerIP = "166.111.140.57"
        self.ServerPort = 8000
        self.SocketHandler = None

    def ConnectionInit(self, host,port):
        self.host = host
        self.port = port
        self.SocketHandler = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = (self.ServerIP,self.ServerPort)
        self.SocketHandler.connect(address)
    
    def SendCommand(self,command):
        self.SocketHandler.send(command.encode())

        reply = self.SocketHandler.recv(512)
        return reply.decode()

    def Login(self,StudentNum,Password):
        command = StudentNum +'_'+Password;
        reply=self.SendCommand(command)
        if reply=="lol":
            return True
        else:
            return False

    def Logout(self,StudentNum):
        command = "logout"+StudentNum
        reply = self.SendCommand(command)
        if reply=="loo":
            return True
        else:
            return False
    
    def GetIp(self,StudentNumList):
        IPlist = []
        for i, stdnum in enumerate(StudentNumList):
            tmpIP = self.SendCommand('q'+stdnum)
            IPlist.append(tmpIP)
        return IPlist    
        
