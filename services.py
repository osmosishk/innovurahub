import sys
from bluepy.btle import UUID, Peripheral

device='9c:a5:25:d8:1e:c9'

p = Peripheral(device,"public")

services=p.getServices()

#displays all services
for service in services:
   print (service)