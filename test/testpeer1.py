import sys
import socket   
sys.path.append('../')
import utility.connectiontool as ctl
s = ctl.ConnectionTool()
s.ConnectionInit("0.0.0.0",50001)

listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listening_socket.bind(("183.172.156.123",9875))
listening_socket.listen(1)

if s.Login("2017011552","net2019"):
    print("login!")

IPlist = s.GetIp(["2017011552","3017011552"])
while True:
    connection, address = listening_socket.accept()
    print("Established connection with: ", address)
    message = connection.recv(512).decode()
    print("Recv: ", message)
    message = connection.recv(512).decode()
    print("Recv: ", message)
    if message == 'quit':
        break;



if s.Logout("2017011552"):
    print("logout")