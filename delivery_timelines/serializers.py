# MongoDB codex packages; should be available in most python distributions
from . import models
from rest_framework import serializers
from package_info.models import Package
from delivery_timelines.models import Status
from django.core.exceptions import ObjectDoesNotExist
from devices.models import Hub, Drone
from users.models import User
import logging
from django.conf import settings
import sys

if settings.DEBUG:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S')
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S')

class StatusSerializer(serializers.ModelSerializer):
	logging.debug('In StatusSerializer')

	class Meta:
		model = Status
		fields = '__all__'

class HubSerializer(serializers.ModelSerializer):
	logging.debug('in HubSerializer')

	class Meta:
		model = Hub
		fields = ['name',]
class DroneSerializer(serializers.ModelSerializer):
	logging.debug('in DroneSerializer')

	class Meta:
		model = Drone
		fields = ['name',]

class SenderSerializer(serializers.ModelSerializer):
	logging.debug('in SenderSerializer')

	class Meta:
		model = User
		fields = ('name',)
class ReceiverSerializer(serializers.ModelSerializer):
	logging.debug('in SenderSerializer')

	class Meta:
		model = User
		fields = ('name',)
class DriverSerializer(serializers.ModelSerializer):
	logging.debug('in SenderSerializer')

	class Meta:
		model = User
		fields = ('name',)
	def get_dump_object(self, obj):
		mapped_object = {
            'name': obj.name,
        }
		return mapped_object

class PackageSerializer(serializers.ModelSerializer):
	logging.debug('in PackageSerializer')

	status = StatusSerializer(read_only=True)
	hub = HubSerializer(read_only=True)
	drone = DroneSerializer(read_only=True)
	sender = SenderSerializer(read_only=True, many=True)
	receiver = ReceiverSerializer(read_only=True, many=True)
	driver = DriverSerializer(read_only=True, many=True)
	class Meta:
		model = Package
		fields = ('id','name','hub','drone', 'sender','receiver','driver','order_date','status')
		# fields = '__all__'