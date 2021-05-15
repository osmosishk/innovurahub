import sys
from bluepy.btle import Peripheral ,DefaultDelegate , Scanner
import binascii
from struct import unpack
import time
import binascii
from bluepy import btle
import threading
from multiprocessing import Process, Event


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)




class BLEScanner:
    def __init__(self):
        self.scanner = Scanner().withDelegate(ScanDelegate())

        self.stop_event = Event()

    def start(self):

        self.stop_event.clear()

        self.process = Process(target=self.scan, args = ())
        self.process.start()
        return self

    def scan(self):
        while True:

            if self.stop_event.is_set():
                return

            self.devices = self.scanner.scan(5, passive=True)

    def stop(self):
        self.stop_event.set()


BLE_ADDRESS='9c:a5:25:d8:1e:c9'
BLE_SERVICE_UUID ="0003cdd0-0000-1000-8000-00805f9b0131"
BLE_CHARACTERISTIC_UUID= "0003cdd1-0000-1000-8000-00805f9b0131"

bt_addrs = []
connections = []
connection_threads = []
scanner = Scanner(0)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self , number):
        btle.DefaultDelegate.__init__(self)
        print("handleNotification init")
        self.number = number


    def handleNotification(self, cHandle, data):

        print ("Developer: do what you want with the data.")
        print (data)


class ConnectionHandlerThread (threading.Thread):
    def __init__(self, connection_index):
        threading.Thread.__init__(self)
        self.connection_index = connection_index

    def run(self):
        print("Thread Connecting...%s",self.connection_index)
        connection = connections[self.connection_index]
        connection.setDelegate(MyDelegate(self.connection_index))
        time.sleep(1.0)

        while True:
            if connection.waitForNotifications(1):
                print("Notification trigger")
                handle = 15
                connection.writeCharacteristic(handle, b'\x01\x00', withResponse=True)






#print ("Connecting...")
#dev = btle.Peripheral(BLE_ADDRESS)
#dev.setDelegate(MyDelegate(1))


#handle=15
#dev.writeCharacteristic(handle,b'\x01\x00', withResponse=True)



time.sleep(1.0)  # Allow sensor to stabilise

while True:
    print ('Connected: ' + str(len(connection_threads)))
    print('Scanning…')

    #BLEScanner().start()
    devices = scanner.scan(2)

    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if (desc == "Complete Local Name") and (value == "Innovura_IOT"):
                #print("  %s = %s" % (desc, value))

                if dev.addr in bt_addrs:
                    print("Device IN list %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                    p = btle.Peripheral(dev.addr)

                    connections.append(p)
                    t = ConnectionHandlerThread(len(connections)-1)
                    t.start()
                    connection_threads.append(t)

                else:
                    bt_addrs.append(dev.addr)
                    print("Device just added  %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))







