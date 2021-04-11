from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse , JsonResponse
import datetime
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, PeriodicTasks

from datetime import date


from slaves_app.models import Setting, MemoryZone, Slave, DataHistory
from slaves_app.serializers import SettingSerializer, SlaveSerializer, MemoryZoneSerializer,DataHistorySerializer
from . import my_own_lib
from .functions import \
    get_slaves_the_client_is_looking_for, convert_list_of_slaves_to_json_format, \
    link_memory_zones_with_their_slave_in_a_json_format, get_all_memory_zones_for_each_slave_in_json_format


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


class MemoryZoneViewSet(viewsets.ModelViewSet):
    queryset = MemoryZone.objects.all()
    serializer_class = MemoryZoneSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(MemoryZoneViewSet, self).get_serializer(*args, **kwargs)




class SlaveViewSet(viewsets.ModelViewSet):
    queryset = Slave.objects.all()
    serializer_class = SlaveSerializer




# Todo  we have to allow only the get

class DataHistoryViewSet(viewsets.ModelViewSet):
    queryset = DataHistory.objects.all()
    serializer_class = DataHistorySerializer

    def get_queryset(self):
        start_date = datetime.date(2020,9,20)
        end_date = datetime.date(2020,9,21)
        queryset = self.queryset
        query_set = queryset.filter(time__range=(start_date, end_date))

        return query_set


@api_view(['GET'])
def showdata(request,job_id):

    if request.method == 'GET' and 'start_day' in request.GET:
        start_day = request.GET["start_day"]
        end_day = request.GET["end_day"]

        print(start_day)
        print(end_day)
        tasks = DataHistory.objects.filter(time__range=(start_day, end_day), jobid=job_id)

    else:
        tasks = DataHistory.objects.filter(jobid=job_id).order_by('-id')[:10]

    serializer = DataHistorySerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def showinstantdata(request,job_id):

    tasks = DataHistory.objects.filter(jobid=job_id).order_by('-id')[:5]
    serializer = DataHistorySerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def deletedata(request,job_id):

    if request.method == 'POST' and 'start_day' in request.GET:
        start_day = request.GET["start_day"]
        end_day = request.GET["end_day"]

        print(start_day)
        print(end_day)
        DataHistory.objects.filter(time__range=(start_day, end_day), jobid=job_id).delete()

    else:
        tasks = DataHistory.objects.filter(jobid=job_id).delete()

    data = {'record_active': True}
    return JsonResponse(data)



@api_view(['GET'])
@transaction.atomic
def look_for_slaves(request):
    slaves = get_slaves_the_client_is_looking_for(request)
    memory_zones_json = get_all_memory_zones_for_each_slave_in_json_format(slaves)
    slaves_in_json = convert_list_of_slaves_to_json_format(slaves)
    slaves_in_json = link_memory_zones_with_their_slave_in_a_json_format(slaves_in_json,
                                                                         memory_zones_json)
    return Response(slaves_in_json)

@api_view(['GET','POST'])
def start(request):
    if request.method == 'GET':
        now = datetime.datetime.now()
        html = "<html><body>Start Datalogger , It is now %s.</body></html>" % now
        return HttpResponse(html)

    if request.method == 'POST':
        task = PeriodicTask.objects.get(name='every-15-seconds')
        task.enabled = True
        task.save()
        data = {'is_active': True}
        return JsonResponse(data)


    return HttpResponse(status=201)

@api_view(['GET','POST'])
def dataloggerstatus(request):


    if request.method == 'GET':
        task = PeriodicTask.objects.get(name='every-15-seconds')
        print(task.enabled)
        data = {'status': task.enabled}
        return JsonResponse(data)


    return HttpResponse(status=201)


@api_view(['GET','POST'])
def stop(request):
   

    if request.method == 'GET':
        now = datetime.datetime.now()
        html = "<html><body>Stop Datalogger ,It is now %s.</body></html>" % now
        return HttpResponse(html)

    if request.method == 'POST':
        task = PeriodicTask.objects.get(name='every-15-seconds')
        task.enabled = False
        task.save()
        data = {'is_active': False}
        return JsonResponse(data)



    return HttpResponse(status=201)


@api_view(['GET', 'POST'])
def slaveenable(request,slave_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        html = "<html><body>Slave Enable ,It is now %s.</body></html>" % now
        return HttpResponse(html)

    if request.method == 'POST':
        Slave.objects.filter(slave_address=slave_id).update(enable=True)
        data = {'is_active':True}
        return JsonResponse(data)

    return HttpResponse(status=201)

@api_view(['GET', 'POST'])
def slavedisable(request,slave_id):
    if request.method == 'GET':
        now = datetime.datetime.now()
        html = "<html><body>Slave Enable ,It is now %s.</body></html>" % now
        return HttpResponse(html)

    if request.method == 'POST':
        Slave.objects.filter(slave_address=slave_id).update(enable=False)

        data = {'is_active':False}
        return JsonResponse(data)

    return HttpResponse(status=201)