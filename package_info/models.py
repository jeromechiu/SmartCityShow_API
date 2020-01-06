# -*- coding: utf-8 -*-

from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class Package(models.Model):
	package_id = models.CharField(max_length=100)
	sender = models.CharField(max_length=100)
	receiver = models.CharField(max_length=100)
	driver = models.CharField(max_length=100)
	order_date = models.DateTimeField('寄送時間',default = timezone.now)

	def __str__(self):
		return self.package_id

	# def get_absolute_url(self):
	# 	return "/package/%i/" % self.package_id

	class Meta:
		ordering = ["order_date"]

