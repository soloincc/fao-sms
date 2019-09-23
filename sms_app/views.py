from .common_tasks import Terminal

terminal = Terminal()


def index(request):
    terminal.tprint('The application is well initialized...', 'debug')
