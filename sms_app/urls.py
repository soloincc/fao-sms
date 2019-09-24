# from django.contrib import admin
from django.conf.urls import url

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.conf import settings
from sms_app import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^callback', views.process_callbacks, name='process_callbacks'),
]
