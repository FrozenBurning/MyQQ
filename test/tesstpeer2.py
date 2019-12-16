import sys
import socket
sys.path.append('../')
import utility.connectiontool as ctl
s = ctl.ConnectionTool()
s.ConnectionInit("127.0.0.1",50000)

listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listening_socket.bind(("127.0.0.1",9876))
listening_socket.listen(1)

if s.Login("3017011552","net2019"):
    print("login!")

IPlist = s.GetIp(["2017011552","3017011552"])

p2psocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if IPlist[0] != 'n':
    p2psocket.connect((IPlist[0],9875))
    p2psocket.send("hhh".encode())
    
    p2psocket.send("quit".encode())
    p2psocket.close()

if s.Logout("2017011552"):
    print("logout")