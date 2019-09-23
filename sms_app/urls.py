# from django.contrib import admin
from django.conf.urls import url

# from django.conf import settings
from sms_app import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
]
