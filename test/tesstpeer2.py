import sys
import socket
import time
sys.path.append('../')

import utility.connectiontool as ctl
import Chatter.listener as listener
import Chatter.sender as sender

s = ctl.ConnectionTool()
s.ConnectionInit("127.0.0.1",50000)

chatlisten = listener.ChatListener()
chatlisten.port = 9876
chatlisten.start()

if s.Login("3017011552","net2019"):
    print("login!")

while True:
    time.sleep(1.0)
    IPlist = s.GetIp(["2017011552","3017011552"])
    if IPlist[0] != 'n':
        break
    
chatsender = sender.ChatSender()
chatsender.address = IPlist[0]
chatsender.port = 9875
chatsender.srcid = "3017011552"
chatsender.desid = "2017011552"
chatsender.start()

# if s.Logout("3017011552"):
#     print("logout")