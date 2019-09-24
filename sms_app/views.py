import json

from .common_tasks import Terminal
from django.http import HttpResponse

terminal = Terminal()


def index(request):
    terminal.tprint('The application is well initialized...', 'debug')


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
