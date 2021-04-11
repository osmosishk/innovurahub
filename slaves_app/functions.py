import minimalmodbus
from django.conf import settings
from slaves_app import my_own_lib
from slaves_app.models import Slave , DataHistory
from slaves_app.serializers import MemoryZoneSerializer, SlaveSerializer
import redis
import json

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT, db=0)

def read_sensors_values(slaves):
    for slave in slaves:
        #read_register_address(slave)
        read_register_address_json(slave)


def read_register_address(slave):
    slave_instrument = create_slave_instrument(slave)
    slave_register_address= slave.get_register_address()
    [print(each_address.read_value(slave_instrument)) for each_address in slave_register_address]

def read_register_address_json(slave):
    data= {}

    slave_instrument = create_slave_instrument(slave)    # create Modbus Slave
    slave_register_address= slave.get_register_address() # read each address of each slave

    for each_address in slave_register_address:
        fieldname = each_address.get_fieldname()
        units = each_address.get_unit()
        value =each_address.read_value(slave_instrument)
        data[fieldname]=value

    ##json_input = json.dumps(data)
    ##redis_instance.lpush(slave.job_id, json_input)



    print(data)
    DataHistory.objects.create(slaveid = slave.slave_address ,jobid=slave.job_id, data=data).save()



def create_slave_instrument(slave):
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slave.slave_address)
    instrument.serial.baudrate = slave.setting.baudrate
    instrument.serial.parity = slave.setting.parity
    instrument.serial.stopbits = slave.setting.stopbits
    instrument.serial.bytesize = slave.setting.bytesize
    instrument.serial.timeout = slave.setting.timeout
    instrument.mode = minimalmodbus.MODE_RTU
    return instrument


def get_slaves_the_client_is_looking_for(request):
    keyword = request.GET.get('search', '')
    slaves_with_redundancy = Slave.get_slaves_with_name_or_mac_or_address_start_with(keyword=keyword)
    slaves = my_own_lib.remove_redundancy_items_from_the_list(queryset=slaves_with_redundancy)
    return slaves


def get_all_memory_zones_for_each_slave_in_json_format(slaves):
    memory_zones = []
    for slave in slaves:
        memory_zones.append(MemoryZoneSerializer(list(slave.get_memory_zones()), many=True))
    return memory_zones


def convert_list_of_slaves_to_json_format(slaves):
    slaves_serialized = SlaveSerializer(slaves, many=True)
    slaves_in_json = slaves_serialized.data
    return slaves_in_json


def link_memory_zones_with_their_slave_in_a_json_format(slaves_in_json, memory_zones_json):
    for i in range(0, len(slaves_in_json)):
        slaves_in_json[i]["memory_zone"] = memory_zones_json[i].data
    return slaves_in_json
