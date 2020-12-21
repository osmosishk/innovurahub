from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import transaction
from rest_framework import serializers, status
from django.http import JsonResponse

from .models import *


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('baudrate', 'parity', 'stopbits', 'bytesize', 'timeout')


class MemoryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZone
        fields = ('id', 'slave', 'start_registers_address', 'name', 'unit', 'type_of_value', 'number_of_decimals')
        extra_kwargs = {
            'id': {'required': False, 'read_only': True}
        }

    def create(self, validated_data):
        return MemoryZone.objects.create(**validated_data)


    def update(self, instance, validated_data):
        print(validated_data)

        for key in ['slave', 'start_registers_address', 'name', 'unit', 'type_of_value', 'number_of_decimals']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})



        start_registers_address = validated_data["start_registers_address"]
        name = validated_data["name"]
        unit = validated_data["unit"]
        type_of_value = validated_data["type_of_value"]
        number_of_decimals = validated_data["number_of_decimals"]


        instance.start_registers_address = start_registers_address
        instance.name = name
        instance.unit = unit
        instance.type_of_value = type_of_value
        instance.number_of_decimals = number_of_decimals
        instance.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return JsonResponse({'slave_address_delete': True})


#disable
class MemoryZoneHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryZoneHistory
        fields = ('time_of_picking', 'memory_zone', 'value')



class DataHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHistory
        fields = ('slaveid','time', 'data' )


class SlaveSerializer(serializers.ModelSerializer):
    setting = SettingSerializer(required=True  )

    class Meta:
        model = Slave
        fields = ('job_id','slave_address', 'setting',
                  'name', 'enable', 'mac')

    def create(self, validated_data):
        print(validated_data)
        for key in ["slave_address", 'setting',
                    'name', 'enable', 'mac']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})

        slave_address = validated_data['slave_address']
        setting_data = validated_data.pop("setting")
        name = validated_data["name"]
        enable = validated_data["enable"]
        mac = validated_data["mac"]

        setting = SettingSerializer.create(SettingSerializer(), validated_data=setting_data)
        slave, created = Slave.objects.update_or_create(setting=setting, **validated_data)
        slave.save()

        # solved when we create the slave object the django use this serializer to return the json format to the
        # client , but this give us an error , because the sensor value type is not an attribute for the slave model
        # how using the write_only=True on the sensor value type field , so we are not allowing the serializer to
        # look for the se sensor value type to serialize it and add it to the json format of the slave .
        return slave

    def update(self, instance, validated_data):
        print(validated_data)

        for key in ["slave_address", 'setting',
                    'name', 'enable', 'mac']:
            if key not in validated_data:
                raise serializers.ValidationError({'error': "please make sure to fill the {}".format(key)})


        setting_data = validated_data.pop("setting")
        slave_address=validated_data["slave_address"]
        name = validated_data["name"]
        enable = validated_data["enable"]
        mac = validated_data["mac"]
        slave_setting =instance.setting

        instance.slave_address =slave_address
        instance.name = name
        instance.enable = enable
        instance.mac = mac
        instance.save()


        slave_setting.baudrate = setting_data.get('baudrate',slave_setting.baudrate)
        slave_setting.parity   = setting_data.get('parity',slave_setting.parity)
        slave_setting.stopbits = setting_data.get('stopbits',slave_setting.stopbits)
        slave_setting.bytesize = setting_data.get('bytesize',slave_setting.bytesize)
        slave_setting.timeout  = setting_data.get('timeout',slave_setting.timeout)
        slave_setting.save()

        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return JsonResponse({'slave_delete': True})
