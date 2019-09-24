# from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

# from django.conf import settings
from sms_app import views
# from .models import SMSQueue

router = routers.DefaultRouter()
# {'post': 'put'}
# router.register('smsqueue', views.process_at_callbacks, basename='SMSQueue')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^smsqueue', views.process_at_callbacks, name='process_at_callbacks'),
    url('nexmo/', views.process_nexmo_callbacks, name='process_nexmo_callbacks'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
