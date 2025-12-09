
import json
from django.core import serializers 
from django.http import JsonResponse
from django.shortcuts import render
from pathlib import Path
from apps.sensors.models import Sensors, Devices, DevicesView
from django.http import HttpResponse
from django.views import View
from django.db.backends.base.base import logger
from django.db import connection

def QuerySetConvertToJson(queryset):
    list_of_dicts = list(queryset)
    json_dumps = json.dumps(list_of_dicts)
    json_string = json.loads(json_dumps)
    data = json_string
    return data

def __init__(self, name, age):
    self.name = name
    self.age = age

def index(request):
    db_sensors_data = QuerySetConvertToJson(Sensors.objects.all().values())
    db_devices_data = QuerySetConvertToJson(Devices.objects.all().values())
    db_devicesView_data = QuerySetConvertToJson(DevicesView.objects.all().values("device_name", 
                                                                                 "device_properties_name", 
                                                                                 "device_properties_note", 
                                                                                 "device_properties_value"))
    
    # Sensors.objects.filter(id="3").delete() # работает
    # Sensors.objects.filter(id="2").update(title="Hello Hello Hello") # работает
    # Sensors.objects.create(id="3", title="OK") # работает
    
    #q = Sensors.objects.filter(id="1").first()  
    q = Sensors.objects.filter(title__contains="H")
    for sensor in q:
        print(f"{sensor.title}")
    
    '''  
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM view_devices")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        data = [] 
        for row in rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            data.append(row_dict)
    '''
            
    context = {
        "sensors": db_sensors_data,
        "devices": db_devices_data,
        "devicesView": db_devicesView_data
    }
    return render(request, "index.html", context)
    


'''def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})'''
    
'''

'''
