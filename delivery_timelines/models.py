# -*- coding: utf-8 -*-

from django.db import models
# from jsonfield import JSONField
from package_info.models import Package
from jsonfield import JSONField

# Create your models here.



class Status(models.Model):
	package_id = models.OneToOneField(
        Package,
        on_delete=models.CASCADE,
        primary_key=True
    )
	status = JSONField()