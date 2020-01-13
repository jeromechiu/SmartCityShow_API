#-*- coding: utf-8 -*-

from rest_framework.views import APIView
import logging
from django.http import HttpResponse,HttpRequest, JsonResponse
from django.views import View
from . import models
from . import serializers
from django.conf import settings
import sys
import json
from package_info.models import Package
from delivery_timelines.models import Status
from rest_framework.renderers import JSONRenderer

if settings.DEBUG:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S')
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S')

# Create your views here.
class StatusAdminView(APIView):
<<<<<<< HEAD
    def post(self, request, *args, **kwargs):
        logging.debug("in post of StatusAdminView")
=======
    def get(self, request, *args, **kwargs):
        logging.debug("in get")
>>>>>>> 18da751fdc90f73d300e1fc02432f0cc9822ce2d
        pid = kwargs['pid']
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(json.dumps(request.data))
                msgid = data['msgid']
                receiver = data['data']['receiver']
                receiver_id = data['data']['id']
                package = Package.objects.filter(receiver=receiver_id).filter(id=pid)
                if len(package) == 0:
                    data = {'msgid':msgid,'data':''}
                    return JsonResponse(data,status=200)
                else:    
                    data = serializers.PackageSerializer(package[0]).data
                    data = {'msgid':msgid,'data':data}
                return JsonResponse(data,status=200)
            except Exception as e:
                logging.debug('JSON decode error: %s', e)
                return HttpResponse(status=403)
        else:
            logging.debug('HTTP Header Method Incorrect')
            return HttpResponse(status=403)