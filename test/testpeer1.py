import sys
import socket   
import time
sys.path.append('../')

import utility.connectiontool as ctl
import Chatter.listener as listener
import Chatter.sender as sender


s = ctl.ConnectionTool()
s.ConnectionInit("0.0.0.0",50001)


chatlisten = listener.ChatListener()
chatlisten.port = 9875
chatlisten.start()
# listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# listening_socket.bind(("183.172.156.123",9875))
# listening_socket.listen(1)

if s.Login("2017011552","net2019"):
    print("login!")

while True:
    time.sleep(1.0)
    IPlist = s.GetIp(["2017011552","3017011552"])
    if IPlist[1] != 'n':
        break

chatsender = sender.ChatSender()
chatsender.address = IPlist[1]
chatsender.port = 9876
chatsender.srcid = "2017011552"
chatsender.desid = "3017011552"
chatsender.start()



# if s.Logout("2017011552"):
#     print("logout")