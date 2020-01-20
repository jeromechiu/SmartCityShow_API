#-*- coding: utf-8 -*-


import logging
import sys
import json
import time
import requests
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from . import models
from django.conf import settings
from package_info.models import Package
from devices.models import Hub
from delivery_timelines.models import Status
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User

if settings.DEBUG:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, \
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', \
    datefmt='%m-%d %H:%M:%S')
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, \
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', \
    datefmt='%m-%d %H:%M:%S')

# Create your views here.
class HubQRAdminView(APIView):
    def post(self, request, *args, **kwargs):
        logging.debug("in post of HubQRAdminView")
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(json.dumps(request.data))
            except json.JSONDecodeError as e:
                logging.debug('JSON decode error: %s', e)
                return HttpResponse(status=403)
            msgid = data['msgid']
            data = data['data']
            if data['key'] != settings.QRCODE_KEY:
                return HttpResponse(status=403)
            else:
                if data['action'] == 'Send':
                    package_id = Package.objects.get(id=data['package_id'])
                    Status.objects.filter(package_id=package_id).delete()
                    t = datetime.utcnow().replace(microsecond=0).isoformat()
                    s = json.dumps({"Driver_Arrival":t})
                    status = Status(package_id=package_id, status=s).save()
                    sendFCM(t, 'driverarrival')
                    time.sleep(5)
                    # add event onto status

                    try:
                        hub = Hub.objects.get(id=data['hub_id'])
                    except ObjectDoesNotExist as e:
                        logging.debug(e)
                    hub_url = 'http://{ip}:{port}/api/v1/hub/opendoor/'.format(ip=hub.ip, port=hub.port)
                    logging.debug("Send Request to Hub at: %s", hub_url)
                    r = requests.get(hub_url, params=request.GET)
                    if r.status_code == 200:
                        t = datetime.utcnow().replace(microsecond=0).isoformat()
                        sendFCM(t, 'opendoor')
                        time.sleep(5)
                        
                        t = datetime.utcnow().replace(microsecond=0).isoformat()
                        s = json.dumps({"package_exhibit":t})
                        status = Status(package_id=package_id, status=s).save()
                        sendFCM(t, 'package_exhibit')
                        return HttpResponse(status=200)
                    else:
                        return HttpResponse(status=500)
                elif data['action'] == 'Get':
                    # package_id = Package.objects.get(id=data['package_id'])
                    # t = datetime.utcnow().replace(microsecond=0).isoformat()
                    # s = json.dumps({"Receiver_Arrival":t})
                    # status = Status(package_id=package_id, status=s).save()
                    # time.sleep(5)
                    # # add event onto status
                    try:
                        hub = Hub.objects.get(id=data['hub_id'])
                    except ObjectDoesNotExist as e:
                        logging.debug(e)
                    hub_url = 'http://{ip}:{port}/api/v1/hub/opendoor/'.format(ip=hub.ip, port=hub.port)
                    logging.debug("Send Request to Hub at: %s", hub_url)
                    r = requests.get(hub_url, params=request.GET)
                    if r.status_code == 200:
                        t = datetime.utcnow().replace(microsecond=0).isoformat()
                        sendFCM(t, 'opendoor')
                        time.sleep(5)
                        package_id = Package.objects.get(id=data['package_id'])
                        print(package_id)
                        status = Status.objects.get(package_id=package_id)
                        t = datetime.utcnow().replace(microsecond=0).isoformat()              
                        s = {"Receiver_Arrival":t}
                        if isinstance(status.status, str):
                            current_s = json.loads(status.status)
                        else:
                            current_s = status.status
                        current_s.update(s)
                        status.status = current_s
                        status.save()
                        sendFCM(t, 'receiverarrival')
                        time.sleep(5)
                        return HttpResponse(status=200)
                else:
                    logging.debug('Incorrect action')
                    return HttpResponse(status=403)
        else:
            logging.debug('HTTP Content-Type Incorrect')
            return HttpResponse(status=403)
            
class DroneTakeoffAdminView(APIView):
    def get(self, request, *args, **kwargs):
        logging.debug("in get of DroneTakeoffAdminView")
        hid = kwargs['hid']
        pid = kwargs['pid']
        if addStatus(pid, "package_onmission") == "None":
            return HttpResponse(status=500)
        return HttpResponse(status=200)


class DroneArrivalAdminView(APIView):
    def get(self, request, *args, **kwargs):
        logging.debug("in get of DroneArrivalAdminView")
        hid = kwargs['hid']
        pid = kwargs['pid']
        if addStatus(pid, "package_arrival") == "None":
            return HttpResponse(status=500)
        return HttpResponse(status=200)


class DroneGotAdminView(APIView):
    def get(self, request, *args, **kwargs):
        logging.debug("in get of DroneGotAdminView")
        hid = kwargs['hid']
        pid = kwargs['pid']
        if addStatus(pid, "package_got") == "None":
            return HttpResponse(status=500)
        return HttpResponse(status=200)

class UploadFCMTokenAdminView(APIView):
    def post(self, request, *args, **kwargs):
        logging.debug("in post of UploadFCMTokenAdminView")
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(json.dumps(request.data))
            except json.JSONDecodeError as e:
                logging.debug('JSON decode error: %s', e)
                return HttpResponse(status=403)
            msgid = data['msgid']
            data = data['data']
            from fcm_django.models import FCMDevice
            try:
                device = FCMDevice.objects.get(device_id=data['device_id'])
            except ObjectDoesNotExist as e:
                u = User.objects.filter().first()
                FCMDevice(name=data['name'], active=True, user=u, device_id=data['device_id'], registration_id=data['registration_id'], type='android').save()
            return HttpResponse(status=200)
        else:
            logging.debug('HTTP Content-Type Incorrect')
            return HttpResponse(status=403)





def addStatus(package_id, status_key):
    package_id = Package.objects.get(id=package_id)
    status = Status.objects.get(package_id=package_id)
    t = datetime.utcnow().replace(microsecond=0).isoformat()
    s = {status_key:t}
    if isinstance(status.status, str):
        current_s = json.loads(status.status)
    else:
        current_s = status.status
    current_s.update(s)
    status.status = current_s
    status.save()
    sendFCM(t, status_key)
    return status



def sendFCM(time, status_key):
    keyword = {
        'package_onmission':'Package on the air',
        'package_arrival':'Package arrival',
        'package_got':'Package already got',
        'package_land':'Drone Landing',
        'package_exhibit':'Package Exhibiting',
        'opendoor':'Door Opened',
        'driverarrival':'Driver Arrival',
        'receiverarrival':'Receiver Arrival'
    }
    from fcm_django.models import FCMDevice
    device = FCMDevice.objects.all()
    logging.debug(device)
    s = '{time} {status}'.format(time=time, status=keyword[status_key])
    try:
        device.send_message(title="CiRC", icon='@mipmap-xxxhdpi/drone_pin',body=s,color = "#391089")
    except Excetion as e:
        logging.debug(e)
    return True