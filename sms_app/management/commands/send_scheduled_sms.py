from django.core.management.base import BaseCommand
from sms_app.sms_queue import FAOSMSQueue


class Command(BaseCommand):
    help = 'Sends the queued SMS in the database. You can specify the provider to use in sending the message'

    def add_arguments(self, parser):
        parser.add_argument('--provider', nargs='?', type=str)

    def handle(self, *args, **options):
        if 'provider' in options:
            if options['provider'] is None:
                print("No default provider selected. The bulk SMS will be spread across the defined providers")
            else:
                print("Requested to use '%s' as the default provider" % options['provider'])
            provider = options['provider']
        else:
            provider = None

        queue = FAOSMSQueue()
        if provider == 'at':
            queue.configure_at()
        queue.process_scheduled_sms(provider)
