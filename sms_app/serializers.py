from rest_framework import serializers

from .models import SMSQueue


class SMSQueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SMSQueue
        fields = ['delivery_time', 'msg_status', 'provider_id']
