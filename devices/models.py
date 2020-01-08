# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator


class Hub(models.Model):
	id = models.AutoField(primary_key=True,unique=True)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=300)
	ip = models.GenericIPAddressField()
	port = models.IntegerField(validators=[
            MaxValueValidator(50000),
            MinValueValidator(2000)
        ])
	def __str__(self):
		return str(self.id)
	# def return_hub_name(self):
	# 	return self.name
	class Meta:
		pass

class Drone(models.Model):
	id = models.AutoField(primary_key=True,unique=True)
	name = models.CharField(max_length=100)
	hub_id = models.ForeignKey(Hub, on_delete=models.SET_NULL,null=True, blank=True)
	def __str__(self):
		return str(self.id)
		
	class Meta:
		pass
