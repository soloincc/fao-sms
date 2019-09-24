"""The main processing unit

This module contains the core functions in the sms queue
"""
import json
import csv
import re
import datetime
import uuid
import pytz

from faker import Faker
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from raven import Client

from .common_tasks import Terminal
from .models import SMSQueue, MessageTemplates, Recepients, Campaign

terminal = Terminal()
sentry = Client(settings.SENTRY_DSN)

settings.TIME_ZONE
current_tz = pytz.timezone(settings.TIMEZONE)
timezone.activate(current_tz)


class FAOSMSQueue():
    def __init__(self):
        # silence is golden
        self.time_formats = ['now', 'today', 'tomorrow', 'yesterday']

    def process_test_data(self, input_file):
        """Given an input file, imports the data to the DB

        Allows initialization of base data to the database.
        """
        terminal.tprint('Processing the file %s...' % input_file, 'info')

        try:
            transaction.set_autocommit(False)
            with open(input_file, 'rt') as in_file:
                test_data = csv.DictReader(in_file, delimiter=',', quotechar='"')
                for row in test_data:
                    self.process_test_message(row)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            sentry.captureException()
            terminal.tprint(str(e), 'fail')

        terminal.tprint("The input file '%s' with test data has been processed successfully..." % input_file, 'info')

    def process_test_message(self, mssg):
        # if the message to be sent is empty, just ignore the line
        if mssg['message'].strip() == '':
            terminal.tprint('We have an empty message, nothing to do here...', 'info')
            return

        # generate the message uuid
        mssg_uuid = uuid.uuid5(uuid.NAMESPACE_X500, mssg['message'])

        # check if we need to add a campaign
        if mssg['campaign'] != '':
            try:
                cur_campaign = Campaign.objects.filter(campaign_name=mssg['campaign']).get()
            except Campaign.DoesNotExist:
                cur_campaign = self.save_campaign(mssg['campaign'])
        else:
            cur_campaign = None

        # check if we have a sending time
        cur_time = timezone.localtime(timezone.now())
        # print(mssg['sending_time'])
        if mssg['sending_time'] != '':
            mssg_sending_time = mssg['sending_time'].strip()
            # check if the data specified is correct, else throw an error
            if mssg_sending_time in self.time_formats:
                if mssg_sending_time == 'now' or mssg_sending_time == 'today':
                    schedule_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')
                elif mssg_sending_time == 'tomorrow':
                    schedule_time = (cur_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                elif mssg_sending_time == 'yesterday':
                    schedule_time = (cur_time + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                try:
                    schedule_time = timezone.datetime.strptime(mssg['sending_time'], '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    terminal.tprint(str(e), 'fail')
                    raise ValueError("Incorrect sending time specified. The sending time can only be '%s' or a valid date time string eg. 2019-09-23 14:41:00" % ', '.join(self.time_formats))
        else:
            schedule_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')

        # check if the message is already added to the template
        try:
            msg_template = MessageTemplates.objects.filter(uuid=mssg_uuid, campaign=cur_campaign).get()
        except MessageTemplates.DoesNotExist:
            msg_template = self.add_message_template(mssg['message'], mssg_uuid, cur_campaign)

        # split the recepients of the message and add to the queues
        for rec in mssg['recepient_nos'].split(','):
            rec = rec.strip()
            if len(rec) == 0:
                continue

            try:
                recepient = Recepients.objects.filter(recepient_no=rec).get()

                # check if a similar messa

                # everything is now really good... so lets add this to the queue
                # Django saves all the dates and times to the database in the UTC timezone
                queue_item = SMSQueue(
                    template=msg_template,
                    message=mssg['message'].strip(),
                    recepient=recepient,
                    recepient_no=rec,
                    msg_status='SCHEDULED',
                    schedule_time=schedule_time
                )
                queue_item.full_clean()
                queue_item.save()
            except Recepients.DoesNotExist:
                recepient = self.add_recepient(rec)
            except Exception as e:
                terminal.tprint(str(e), 'fail')
                sentry.captureException()
                raise Exception(str(e))

    def save_campaign(self, campaign_name):
        """Save a campaign since it does not exist

        Returns:
            The campaign object which has been created
        """
        try:
            cur_campaign = Campaign(
                campaign_name=campaign_name
            )
            cur_campaign.full_clean()
            cur_campaign.save()

            return cur_campaign
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()
            raise

    def add_recepient(self, recepient_no, first_name=None, other_names=None):
        """Adds a recepient to the database since they don't exist

        The recepient does not exist, so lets add to them to the database

        Args:
            recepient_no (string): the phone number of the recepient
            first_name (string | optional): the first name
            other_names (string | optional): the other names of the reepient

        Returns:
            Returns the created recepient
        """

        try:
            # if the names haven't been provided, using a faker, populate placeholder names
            if first_name is None:
                fake_p = Faker()
                first_name = fake_p.name().split(' ')[0]
            if other_names is None:
                other_names = fake_p.name().split(' ')[1]

            recepient = Recepients(
                recepient_no=recepient_no,
                first_name=first_name,
                other_names=other_names
            )
            recepient.full_clean()
            recepient.save()
            return recepient
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()
            raise Exception(str(e))

    def add_message_template(self, template, uuid, campaign):
        """Adds a message template to the database

        Adds a message template to the database since it does not exist

        Args:
            template (string): The message template to add to the database
            campaign (Campaign or None): The campaign to associate the message to

        Returns:
            Returns the saved campaign
        """

        try:
            mssg_template = MessageTemplates(template=template, uuid=uuid)
            if campaign is not None:
                mssg_template.campaign = campaign

            mssg_template.full_clean()
            mssg_template.save()

            return mssg_template
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()
            raise Exception(str(e))

    def process_scheduled_sms(self, provider):
        """Processes the scheduled SMS and puts them in the sending queue

        Fetches all the scheduled SMSes from the databases and adds them to a sending queue
        """

        cur_time = timezone.localtime(timezone.now())
        cur_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')
        print(cur_time)
        try:
            gateway_ids = list(settings.SMS_GATEWAYS['gateways'].keys())
            if provider not in gateway_ids:
                raise Exception("'%s' is not configured as a gateway provider. Select from '%s'" % (provider, ', '.join(gateway_ids)))
            # fetch the sms whose sending schedule time has passed
            sms2send = SMSQueue.objects.filter(schedule_time__lte=cur_time, msg_status='SCHEDULED').all()
            for sched_sms in sms2send:
                # print('%s: %s - %s' % (sched_sms.id, sched_sms.schedule_time, sched_sms.recepient_no))
                if provider == 'at':
                    self.send_via_at(sched_sms)
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()

        # def queue_via_at(self, mssg):

    def configure_at(self):
        """Configures and initializes AfricasTalking as an SMS gateway provider

        Using the settings provided in the settings file, configures and initializes AT as an SMS gateway
        """
        import africastalking

        print(settings.SMS_GATEWAYS['gateways']['at']['KEY'])
        username = settings.SMS_GATEWAYS['gateways']['at']['USERNAME']
        api_key = settings.SMS_GATEWAYS['gateways']['at']['KEY']
        africastalking.initialize(username, api_key)
        self.at_sms = africastalking.SMS

    def send_via_at(self, mssg):
        """Submits a message to be sent via the AT gateway
        
        Args:
            The message object as JSON to be sent
        """
        try:
            # queue the message to be sent via africastalking. Once queued, update the database with the queue status
            cur_time = timezone.localtime(timezone.now())
            cur_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')
            # lets send the messages synchronously... should be changed to async
            # How does AT identify a message when a callback is given
            this_resp = self.at_sms.send(mssg.message, [mssg.recepient_no], enqueue=False)
            mssg.in_queue = 0
            mssg.queue_time = cur_time
            mssg.msg_status = settings.AT_STATUS_CODES[this_resp['SMSMessageData']['Recipients'][0]['statusCode']]
            mssg.provider_id = this_resp['SMSMessageData']['Recipients'][0]['messageId']
            mssg.save()
            # print(this_resp)
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()
            raise Exception(str(e))

    def process_at_delivery_report(self, report):
        try:
            print(report)
        except Exception as e:
            terminal.tprint(str(e), 'fail')
            sentry.captureException()
            raise Exception(str(e))


def process_at_response(error, response):
    print(response)
    if error is not None:
        raise Exception(error)

    for resp in response['SMSMessageData']['Recipients']:
        # get this message which was queued and update its status
        # mssg = SMSQueue.objects.filter(schedule_time__lte=cur_time, msg_status='SCHEDULED').all()
        print(resp)
