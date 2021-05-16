from bluepy import btle
import struct, os
from concurrent import futures
from bluepy.btle import Scanner, DefaultDelegate
global addr_var
global delegate_global
global perif_global

import json
from datetime import datetime
import socket
iot_host = socket.gethostname()
import requests
url = 'http://192.46.225.215:8080'
headers = {"content-type : ": "application/json"}
addr_var = ['9c:a5:25:df:c6:3c', '9c:a5:25:df:fc:f3', '9c:a5:25:d8:1e:c9']
#addr_var=[]

#file_in = open("device.json", "r")
#for line in file_in:
#    addr_var.append(line.rstrip('\n'))

#print(addr_var)

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global addr_var
        global delegate_global
        datajson = {}




        for ii in range(len(addr_var)):
            if delegate_global[ii] == self:
                data_decoded = data.decode('utf-8')
                now = datetime.now()
                datajson['iot_host'] = iot_host
                datajson['time'] = now.isoformat()
                datajson['bleaddress'] = addr_var[ii]
                #print("Address2: " + addr_var[ii])
                #print(data_decoded)
                result = data_decoded.split(",")
                for y in result:
                    if (y.split(":", 1)[0] == '1'):
                        datajson['value'] = y.split(":", 1)[1]
                    if (y.split(":", 1)[0] == '2'):
                        datajson['sensor'] = y.split(":", 1)[1]
                    if (y.split(":", 1)[0] == '3'):
                        datajson['battery'] = y.split(":", 1)[1]

                print(datajson)

                response = requests.post(url, json=datajson, auth=('logstash', 'iottest'))

                print("Server responded with %s" % response.status_code)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()


def perif_loop(perif, indx):

    while True:
        try:
            if perif.waitForNotifications(1.0):
                print("Notification trigger")


        except:
            try:
                perif.disconnect()
            except:
                pass
            print("disconnecting perif: " + perif.addr + ", index: " + str(indx))
            reestablish_connection(perif, perif.addr, indx)


delegate_global = []
perif_global = []
[delegate_global.append(0) for ii in range(len(addr_var))]
[perif_global.append(0) for ii in range(len(addr_var))]


def reestablish_connection(perif, addr, indx):
    while True:
        try:
            print("trying to reconnect with " + addr)
            perif.connect(addr)
            print("re-connected to " + addr + ", index = " + str(indx))
            return
        except:
            continue


def establish_connection(addr):
    global delegate_global
    global perif_global
    global addr_var

    while True:
        try:
            for jj in range(len(addr_var)):
                if addr_var[jj] == addr:
                    handle = 15
                    print("Attempting to connect with " + addr + " at index: " + str(jj))
                    p = btle.Peripheral(addr)
                    perif_global[jj] = p
                    p_delegate = MyDelegate(addr)
                    delegate_global[jj] = p_delegate
                    p.withDelegate(p_delegate)
                    p.writeCharacteristic(handle, b'\x01\x00', withResponse=True)
                    print("Connected to " + addr + " at index: " + str(jj))
                    perif_loop(p, jj)
        except:
            print("failed to connect to " + addr)
            continue





ex = futures.ProcessPoolExecutor(max_workers=os.cpu_count())
results = ex.map(establish_connection, addr_var)