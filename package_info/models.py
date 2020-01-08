# -*- coding: utf-8 -*-

from django.db import models
from users.models import User
from devices.models import Drone, Hub
import django.utils.timezone as timezone

# Create your models here.

class Package(models.Model):
	id = models.AutoField(primary_key=True,unique=True)
	name = models.CharField(max_length=500)
	hub = models.ForeignKey(Hub, on_delete=models.SET_NULL,null=True, blank=True)
	drone = models.ForeignKey(Drone, on_delete=models.SET_NULL,null=True, blank=True) 
	sender = models.ManyToManyField(User, related_name='Sender')
	receiver = models.ManyToManyField(User, related_name='Receiver')
	driver = models.ManyToManyField(User, related_name='Driver')
	order_date = models.DateTimeField('寄送時間',default = timezone.now)



	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = ["order_date"]

