# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Hub, Drone

# Register your models here.

class HubAdmin(admin.ModelAdmin):
	model = Hub
	list_display = ('id', 'name','location','ip','port')

admin.site.register(Hub, HubAdmin)


class DroneAdmin(admin.ModelAdmin):
	model = Drone
	list_display = ('id','name','Hub_Name')
	def Hub_Name(self, obj):
		return obj.hub_id.name
admin.site.register(Drone, DroneAdmin)