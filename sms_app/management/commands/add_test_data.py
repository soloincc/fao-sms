from django.core.management.base import BaseCommand
from sms_app.sms_queue import FAOSMSQueue


class Command(BaseCommand):
    help = 'Imports test data/sms into the application. The input file must be a csv delimited by a <comma> and cells quoted by <""> where necessary'

    def add_arguments(self, parser):
        parser.add_argument('input_files', nargs='+', type=str)

    def handle(self, *args, **options):
        queue = FAOSMSQueue()
        for in_file in options['input_files']:
            queue.process_test_data(in_file)
