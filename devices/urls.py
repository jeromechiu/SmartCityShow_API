#-*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
        re_path(r'^(?P<hid>[^/]+)/(?P<pid>[^/]+)/takeoff/$', views.DroneTakeoffAdminView.as_view(), name='DroneTakeoffAdminView'),
        re_path(r'^(?P<hid>[^/]+)/(?P<pid>[^/]+)/packagearrival/$', views.DroneArrivalAdminView.as_view(), name='DroneArrivalAdminView'),
        re_path(r'^(?P<hid>[^/]+)/(?P<pid>[^/]+)/missiondone/$', views.DroneGotAdminView.as_view(), name='DroneGotAdminView'),
        path('', views.HubQRAdminView.as_view(), name='HubQRAdminView'),
        
]