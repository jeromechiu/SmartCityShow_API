# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Status

# Register your models here.

class StatusAdmin(admin.ModelAdmin):
	model = Status
	list_display = [field.name for field in Status._meta.get_fields()]

admin.site.register(Status, StatusAdmin)