
import sys
sys.path.append('../')

from Chatter.user import *

m=MediaServer()
m.start()

time.sleep(3)
c=MediaClient("183.172.155.54")
c.start()

input("kkk")