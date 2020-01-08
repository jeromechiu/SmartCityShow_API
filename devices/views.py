#-*- coding: utf-8 -*-


import logging
import sys
import json
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
                    Status.objects.filter(package_id=data['package_id']).delete()
                    try:
                        hub = Hub.objects.get(id=data['hub_id'])
                    except ObjectDoesNotExist as e:
                        logging.debug(e)
                    hub_url = 'http://{ip}:{port}/api/v1/hub/opendoor/'.format(ip=hub.ip, port=hub.port)
                    logging.debug("Send Request to Hub at: %s", hub_url)
                    r = requests.get(hub_url, params=request.GET)
                    if r.status_code == 200:
                        package_id = Package.objects.get(id=data['package_id'])
                        s = json.dumps({"package_exhibit":datetime.utcnow().isoformat()})
                        status = Status(package_id=package_id, status=s).save()
                        return HttpResponse(status=200)
                elif data['action'] == 'Get':
                    try:
                        hub = Hub.objects.get(id=data['hub_id'])
                    except ObjectDoesNotExist as e:
                        logging.debug(e)
                    hub_url = 'http://{ip}:{port}/api/v1/hub/opendoor/'.format(ip=hub.ip, port=hub.port)
                    logging.debug("Send Request to Hub at: %s", hub_url)
                    r = requests.get(hub_url, params=request.GET)
                    if r.status_code == 200:
                        package_id = Package.objects.get(id=data['package_id'])
                        status = Status.objects.get(package_id=package_id)                    
                        s = {"package_land":datetime.utcnow().isoformat()}
                        if isinstance(status.status, str):
                            current_s = json.loads(status.status)
                        else:
                            current_s = status.status
                        current_s.update(s)
                        status.status = current_s
                        status.save()
                        return HttpResponse(status=200)
                else:
                    logging.debug('Incorrect action')
                    return HttpResponse(status=403)


                
                
            

        else:
            logging.debug('HTTP Header Method Incorrect')
            return HttpResponse(status=403)