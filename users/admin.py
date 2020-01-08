# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Role, User

# Register your models here.

class RoleAdmin(admin.ModelAdmin):
	model = Role
	list_display = ('id','role')

admin.site.register(Role, RoleAdmin)

class UserAdmin(admin.ModelAdmin):
	model = User
	list_display = ('id','name','role')

admin.site.register(User, UserAdmin)