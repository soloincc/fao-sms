# from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

# from django.conf import settings
from sms_app import views

router = routers.DefaultRouter()
router.register(r'smsqueue', views.SMSQueueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^callback', views.process_callbacks, name='process_callbacks'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
