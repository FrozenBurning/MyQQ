import socket
# 与中央服务器的连接工具
class ConnectionTool:
    def __init__(self):
        self.ServerIP = "166.111.140.57"
        self.ServerPort = 8000
        self.SocketHandler = None
        self.desid = 0

    def ConnectionInit(self, host=None,port=None):
        self.host = host
        self.port = port
        self.SocketHandler = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = (self.ServerIP,self.ServerPort)
        self.SocketHandler.connect(address)
    
    # 发送命令模板
    def SendCommand(self,command):
        self.SocketHandler.send(command.encode())
        print("send to server:",command)

        reply = self.SocketHandler.recv(512)
        print("server Reply:",reply)
        return reply.decode()

    def Login(self,StudentNum):
        command = StudentNum +'_net2019'
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
    
    def GetIp(self,StudentNum):
        return self.SendCommand('q'+StudentNum)
        
        
