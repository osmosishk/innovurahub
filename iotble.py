import sys
from bluepy.btle import UUID, Peripheral ,DefaultDelegate
import binascii
from struct import unpack
import time
import binascii
from bluepy import btle


BLE_ADDRESS='9c:a5:25:df:c6:3c'
BLE_SERVICE_UUID ="0003cdd0-0000-1000-8000-00805f9b0131"
BLE_CHARACTERISTIC_UUID= "0003cdd1-0000-1000-8000-00805f9b0131"
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        print("handleNotification init")


    def handleNotification(self, cHandle, data):

        print ("Developer: do what you want with the data.")
        print (data)


print ("Connecting...")
dev = btle.Peripheral(BLE_ADDRESS)
dev.setDelegate(MyDelegate())


handle=15
dev.writeCharacteristic(handle,b'\x01\x00', withResponse=True)



time.sleep(1.0)  # Allow sensor to stabilise

while True:
    if dev.waitForNotifications(5.0):
        print("Notification trigger")
        continue
    print("waiting...")





