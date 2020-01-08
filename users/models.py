# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Role(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    role = models.CharField(max_length=100)
    def __str__(self):
        return self.role

class User(models.Model):
	id = models.AutoField(primary_key=True,unique=True)
	name = models.CharField(max_length=100)
	role = models.ForeignKey(Role, on_delete=models.SET_NULL,null=True, blank=True)


	def __str__(self):
		return str(self.id)

