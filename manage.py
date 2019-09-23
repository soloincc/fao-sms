#!env/bin/python

import os
import sys

if __name__ == '__main__':
    # add our defined settings to the environment settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from settings.base import *

    try:
        import django
        django.setup()

        from django.core.management.commands.runserver import Command as runserver
        runserver.default_port = DEFAULT_PORT
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)
