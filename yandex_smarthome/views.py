import logging
import json
from urllib import response
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
#from data_base.models import view_devices

#logging.basicConfig(filename='esp8266meteo.log',
#                    encoding='utf-8', level=logging.DEBUG)

#logger = logging.getLogger(__name__)

def sensors_data(request):
    json = {"status": 1}
    
    '''data = Sensors(
        scd30_temp=request.GET["scd30_temp"],
        scd30_co2=request.GET["scd30_co2"],
        scd30_h=request.GET["scd30_h"],
    )
    try:
        data.save()
    except:
        json["status"] = 0'''
    return JsonResponse(json)


def oauth_login(request):
    redirect_uri = request.GET.get("redirect_uri", "")
    state = request.GET.get("state", "")
    client_id = request.GET.get("client_id", "")
    scope = request.GET.get("scope", "")

    url = f"{redirect_uri}?code=1234&state={state}&client_id={client_id}&scope={scope}"

    return redirect(url, permanent=True)


def v10(request): # new
    return HttpResponse('OK')


def user_unlink(request): # new
    # return JsonResponse({ "request_id": request.headers.get("X-Request-Id"), "status": HttpResponse('OK'), })
    data = {
        "request_id": request.headers.get("X-Request-Id"),
    }
    # convert dictionary to JSON
    json_data = json.dumps(data)
    # set headers
    headers = HttpResponse('OK')
    # return JSON response
    return response(json_data, headers=headers)


@csrf_exempt
def oauth_token(request):
    json = {
        "access_token": "ACCESS_TOKEN",
        "token_type": "bearer",
        "expires_in": 2592000,
        "refresh_token": "REFRESH_TOKEN",
        "scope": "read",
        "uid": 100101,
        "info": {"name": "User", "email": "info@example.com"},
    }
    return JsonResponse(json)


def user_devices(request):
    json = {
        "request_id": request.headers.get("X-Request-Id"),
        "payload": {
            "user_id": "162652869",
            "devices": [
                {
                    "id": "abc-123",
                    "name": "Метеостанция",
                    "description": "Измеряет температуру и влажность",
                    "room": "спальня",
                    "type": "devices.types.sensor.climate",
                    "custom_data": {
                        "foo": 1,
                        "bar": "two",
                        "baz": False,
                        "qux": [1, "two", False],
                        "quux": {"quuz": {"corge": []}},
                    },
                    "capabilities": [],
                    "properties": _get_properties(),
                    "device_info": {
                        "manufacturer": "Трасса-60",
                        "model": "Трасса-60.Метеостанция",
                        "hw_version": "1.0",
                        "sw_version": "1.0",
                    },
                }
            ],
        },
    }
    return JsonResponse(json)


@csrf_exempt
def user_devices_query(request):
    json = {
        "request_id": request.headers.get("X-Request-Id"),
        "payload": {
            "devices": [
                {"id": "abc-123",
                 "capabilities": [],
                 "properties": _get_properties()}
            ]
        },
    }
    return JsonResponse(json)


def user_action(request): # new
    json = {
        "request_id": request.headers.get("X-Request-Id"),
        "payload": {
            "devices": []
        }
    }
    return JsonResponse(json)


def _get_properties():

    db_data = Sensors.objects.latest("date")

    return [
        {
            "type": "devices.properties.float",
            "retrievable": True,
            "reportable": True,
            "parameters": {
                "instance": "temperature",
                "unit": "unit.temperature.celsius",
            },
            "state": {"instance": "temperature", "value": db_data.scd30_temp},
            "last_updated": db_data.date,
        },
        {
            "type": "devices.properties.float",
            "retrievable": True,
            "reportable": True,
            "parameters": {"instance": "humidity", "unit": "unit.percent"},
            "state": {"instance": "humidity", "value": db_data.scd30_h},
            "last_updated": db_data.date,
        },
        {
            "type": "devices.properties.float",
            "retrievable": True,
            "reportable": True,
            "parameters": {"instance": "co2_level", "unit": "unit.ppm"},
            "state": {"instance": "co2_level", "value": db_data.scd30_co2},
            "last_updated": db_data.date,
        },
    ]
    
    {"request_id": "df6db774-1b55-4887-a4da-c6adebb1c89a", "payload": {"user_id": "162652869", "devices": [
        {"id": "device-iot-wifi_slot", "name": "Esp8266meteo", "type": "devices.types.sensor.climate", "capabilities": [
        {"type": "devices.capabilities.on_off", "retrievable": true, "reportable": false, "parameters": {"split": false}}, 
        {"type": "devices.capabilities.temperature", "retrievable": true, "reportable": true, "parameters": {"instance": "temperature", "unit": "unit.temperature.celsius"}}
        ]}
        ]}}



@csrf_exempt
def refresh(request):
    json = {
        "access_token": "ACCESS_TOKEN",
        "refresh_token": request.POST.get("refresh_token"),
        "token_type": "bearer",
        "expires_in": 2592000,  # 1 month
    }
    return JsonResponse(json)
