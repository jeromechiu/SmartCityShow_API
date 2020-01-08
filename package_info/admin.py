# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Package



# Register your models here.

class PackageAdmin(admin.ModelAdmin):
	model = Package
	list_display = ('id','name','Hub_Name','Drone_Name','Sender_Name','Receiver_Name','Driver_Name','order_date')

	def Hub_Name(self, obj):
		return obj.hub.name
		
	def Drone_Name(self, obj):
		return obj.drone.name

	def Sender_Name(self, obj):
		return ", ".join([child.name for child in obj.sender.all()])
	def Receiver_Name(self, obj):
		return ", ".join([child.name for child in obj.receiver.all()])
	def Driver_Name(self, obj):
		return ", ".join([child.name for child in obj.driver.all()])

admin.site.register(Package, PackageAdmin)