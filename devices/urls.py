#-*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
        path('', views.HubQRAdminView.as_view(), name='HubQRAdminView'),
        # re_path(r'^(?P<pid>[^/]+)/$', views.StatusAdminView.as_view(), name='StatusAdmin'),

]