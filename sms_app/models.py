import datetime

from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator


class TimeModel(models.Model):
    """ A base model to be inherited by other models

    It is envisaged that each model must include time(adding and modification) data. This
    model will contain this definition of time
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Campaign(TimeModel):
    """ Campaign details

    All campaigns details will be saved in this model
    """
    campaign_name = models.CharField(max_length=100, blank=False, unique=True, validators=[
        MaxLengthValidator(100, message='The campaign name must not be more than 100 characters'),
        MinLengthValidator(3, message='The campaign name must be more than 3 chaaracters')
    ])


class MessageTemplates(TimeModel):
    """
    A list of message templates

    A collection of message templates to be sent. The templates can belong to a campaign or not
    """
    template = models.CharField(max_length=5000, blank=False, validators=[
        MaxLengthValidator(5000, message='The template to be sent must not be more than 5000 characters'),
        MinLengthValidator(10, message='The template must be more than 3 characters')
    ])
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, blank=True)


class Recepients(TimeModel):
    """ Message recepients

    A master list of all our recepients. Messages will only be sent to recepients in this list
    """
    names_validator = RegexValidator(regex='^[a-zA-Z]*$', message='A name should only contain letters')
    first_name = models.CharField(max_length=30, null=True, blank=True, validators=[
        MaxLengthValidator(30, message='The first name must be less than 30 characters'),
        names_validator
    ])
    other_names = models.CharField(max_length=100, null=True, blank=True, validators=[
        MaxLengthValidator(100, message='The other names must be less than 100 characters'),
        names_validator
    ])
    recepient_no = models.CharField(max_length=15, blank=False, validators=[
        MaxLengthValidator(15, message='The recepient number must not be more than 15 characters long')
    ])
    recepient_alternative_no = models.CharField(max_length=15, blank=True, validators=[
        MaxLengthValidator(15, message='The recepient alternative number must not be more than 15 characters long')
    ])

    class Meta:
        unique_together = ('recepient_no', 'first_name', 'other_names')


class SMSQueue(TimeModel):
    template = models.ForeignKey(MessageTemplates, on_delete=models.CASCADE)
    # The actual message that will be sent
    message = models.CharField(max_length=5000, blank=False, validators=[
        MaxLengthValidator(5000, message='The message to be sent must not be more than 5000 characters'),
        MinLengthValidator(10, message='The coop name must be more than 3 characters')
    ])
    recepient = models.ForeignKey(Recepients, blank=False)
    # the actual number the message was sent to
    recepient_no = models.CharField(max_length=15, blank=False, validators=[
        MaxLengthValidator(15, message='The recepient number must not be more than 15 characters long')
    ])
    msg_status = models.CharField(max_length=15, blank=False, validators=[
        MaxLengthValidator(15, message='The status must not be more than 15 characters long')
    ])
    schedule_time = models.DateTimeField(auto_now_add=True, blank=False)        # the time the sms is to be sent
    in_queue = models.BooleanField(blank=False, default=0)                      # is the message in the sending queue
    queue_time = models.DateTimeField(auto_now_add=True, blank=True)            # the time the sms was added to the queue
    delivery_time = models.DateTimeField(auto_now_add=True, blank=True)         # the time the sms was delivered to the recepient
