import sys
sys.path.append('../')
import utility.connectiontool as ctl
s = ctl.ConnectionTool()
s.ConnectionInit("127.0.0.1",50000)

if s.Login("2017011552","net2019"):
    print("login!")

print(s.GetIp(["2017011552","2017011539"]))

if s.Logout("2017011552"):
    print("logout")