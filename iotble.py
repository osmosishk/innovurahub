import sys
from bluepy.btle import UUID, Peripheral ,DefaultDelegate
import binascii
from struct import unpack
import time
from bluepy import btle

device='20:05:11:10:0a:52'

class MyDelegate(btle.DefaultDelegate):
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        print("handling notification...")

        if (data[0] == '\x14'):
            self.message = "Connection Lost"
        if (data[0] == '\x06'):
            self.message = "Booting"
        if (data[0] == '0'):
            print("Booting...")
        else:
           print(data)
           print(data[0])





##      print(self)


        ##print(struct.unpack("c",data))


p = btle.Peripheral(device)
p.setDelegate(MyDelegate(0))

while True:
    if p.waitForNotifications(3.0):
        continue
    print("waiting...")





