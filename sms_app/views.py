import json

from .common_tasks import Terminal
from django.http import HttpResponse
from .serializers import SMSQueueSerializer
from .models import SMSQueue
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


terminal = Terminal()


def index(request):
    terminal.tprint('The application is well initialized...', 'debug')


@csrf_exempt
def process_callbacks(request):
    print(request.GET.get('type'))

    for key, value in request.POST.items():
        print("%s: %s" % (key, value))

    return return_json({})


def return_json(mappings):
    to_return = json.dumps(mappings)
    response = HttpResponse(to_return, content_type='text/json')
    response['Content-Message'] = to_return
    return response


class SMSQueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SMSQueue to be viewed or updated.
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = SMSQueue.objects.all()
    serializer_class = SMSQueueSerializer
