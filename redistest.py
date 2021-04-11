import redis

import json

r = redis.StrictRedis(host='127.0.0.01', port=6379, db=0)


images= {"timestamp":"2021-04-09T14:01:310Z",
        "deviceid": "3xfsFDFDD",
        "Voltage A": 219.2,
        "Voltage B": 219.5,
        "Voltage C": 220.4,
        "Current A": 52.5,
        "Current B": 73.5,
        "Current C": 67.2,
        "PF A": 0.0,
        "PF B": 13.0,
        "PF C": 28.0,
        "L1 KVA": 0.0105,
        "L2 KVA": -0.0147,
        "L3 KVA": -0.0147,
        "L1 KW": 0.0,
        "L2 KW": -0.0021,
        "L3 KW": -0.0021,
        "KWH": 32477.0
        }

def write_to_redis():
    json_images = json.dumps(images)
    r.lpush('image', json_images)


def read_from_redis():
    unpacked_images = json.loads(r.lindex('image',0))
    print(unpacked_images)


write_to_redis()
read_from_redis()



