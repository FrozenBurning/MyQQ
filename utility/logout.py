import sys
import socket   
import time
sys.path.append('../')

import utility.connectiontool as ctl
import Chatter.listener as listener
import Chatter.sender as sender
from Chatter.data_type import *

s = ctl.ConnectionTool()
s.ConnectionInit("0.0.0.0",49999)

# s.Login("40k7011552")
# s.Login("2017011552","net2019")

# iplist = s.GetIp(["3017011552","2017011552"])
if s.Logout("2017011552"):
    print("logout")


s.ConnectionInit("0.0.0.0",49999)

if s.Logout("3017011552"):
    print("logout")