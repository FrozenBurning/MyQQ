import sys
import socket   
import time
sys.path.append('../')

import utility.connectiontool as ctl
import Chatter.listener as listener
import Chatter.sender as sender


s = ctl.ConnectionTool()
s.ConnectionInit("0.0.0.0",49999)



if s.Logout("2017011552"):
    print("logout")

if s.Logout("3017011552"):
    print("logout")