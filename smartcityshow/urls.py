"""smartcityshow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from delivery_timelines import urls as status_url
<<<<<<< HEAD
from devices import urls as devices_url
=======
>>>>>>> 18da751fdc90f73d300e1fc02432f0cc9822ce2d

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/v1/mapp/updatestatus/', include(status_url)),
<<<<<<< HEAD
    url('api/v1/hub/checkqr/', include(devices_url)),
=======
>>>>>>> 18da751fdc90f73d300e1fc02432f0cc9822ce2d
]
