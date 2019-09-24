from rest_framework import serializers

from .models import SMSQueue


class SMSQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSQueue
        # fields = ['delivery_time', 'msg_status', 'provider_id']
        fields = ['provider_id']

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        print('this - here')
        
        # smsqueue = SMSQueue.objects.get(pk=instance.id)
        # SMSQueue.objects.filter(pk=instance.id).update(**validated_data)

        return smsqueue
