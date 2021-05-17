from bluepy.btle import Scanner, DefaultDelegate

oldaddr_var= []
newaddr_var= []

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)



with open("device.json", "r") as file_in:
    lines = []
    for line in file_in:
        oldaddr_var.append(line.rstrip('\n'))


print(oldaddr_var)




scanner = Scanner()
devices = scanner.scan(5)

if len(devices) < 1:
    print('No nearby Devices found. Make sure your Bluetooth Connection !')

else:
    for dev in devices:
        for adtype, desc, value in dev.getScanData():
            if (desc == "Complete Local Name") and ((value == "Innovura_IOT") or (value == "WH-BLE 103")):
                if dev.addr in oldaddr_var:
                    print("Device found list %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                else:
                    print("New Device found list %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                newaddr_var.append(dev.addr)






if len(newaddr_var) < 1:
    print('Cannot find Innovura_IOT Mac address.')



textfile = open("device.json", "w")
for element in newaddr_var:
    textfile.write(element + "\n")