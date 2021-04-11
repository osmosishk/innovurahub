import sys
from bluepy.btle import UUID, Peripheral

device='20:05:11:10:0a:52'

p = Peripheral(device,"public")

services=p.getServices()

#displays all services
for service in services:
   print (service)