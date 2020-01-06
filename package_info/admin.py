# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Package

# Register your models here.

class PackageAdmin(admin.ModelAdmin):
	model = Package
	list_display = [field.name for field in Package._meta.get_fields()]

admin.site.register(Package, PackageAdmin)