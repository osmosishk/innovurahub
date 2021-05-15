import json
import datetime
import socket
iot_host = socket.gethostname()
import requests

url = 'http://192.46.225.215:8080'
headers = {'Content-Type': 'application/json',
           'accept':'application/json'}

datajson = {}

datajson['iot_host'] = iot_host
datajson['time'] = datetime.datetime.utcnow()
datajson['bleaddress'] = '9c:a5:25:df:c6:3c'
datajson['value'] ='432432'
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()




json_input = json.dumps(datajson ,default = myconverter)

x = requests.post(url, data=json_input, auth=('logstash', 'iottest') , headers=headers)
print(json_input )

print(x.status_code)
print(x.request.url)
print(x.request.body)
print(x.request.headers)