import json

from .common_tasks import Terminal
from django.http import HttpResponse
from .serializers import SMSQueueSerializer
from .models import SMSQueue
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .sms_queue import FAOSMSQueue

terminal = Terminal()


def index(request):
    terminal.tprint('The application is well initialized...', 'debug')


@csrf_exempt
def process_at_callbacks(request):
    fao_sms = FAOSMSQueue()
    fao_sms.process_at_report(request)

    return return_json({'mssg': 'processed'})


def return_json(mappings):
    to_return = json.dumps(mappings)
    response = HttpResponse(to_return, content_type='text/json')
    response['Content-Message'] = to_return
    return response


class SMSQueueUpdateSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SMSQueue to be viewed or updated.
    """
    queryset = SMSQueue.objects.all()
    serializer_class = SMSQueueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        delivery_type = self.request.query_params.get('type')
        print(self.request.query_params.get('param1'))
        print(delivery_type)

        if delivery_type == 'delivery':
            # we have a delivery report, please process it
            print(self.request.query_params.get('param1'))
            # at_id = self.request.query_params.get('type')
            # id: ATXid_0165ff43a74761f41af40376fe5d7662
            # status: Success
        return []
        # return SMSQueue.objects.all()

