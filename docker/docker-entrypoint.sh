#!/bin/bash
# publish our environment variables
printenv | grep -v "no_proxy" >> /etc/environment
# python -c 'import sys; print sys.path'
cd /opt/fao_sms

# apply the migrations
python manage.py migrate

# add the test data provided
python manage.py add_test_data sms_app/input_sms.csv

## collect statics
# echo "Collecting the static files... I will not post the progress"
# python manage.py collectstatic --noinput --verbosity 0
# echo "Finished collecting the static files"

## create superuser
#python manage.py createsuperuser

## RUN `python manage.py migrate auth` before running this:
python manage.py shell << EOF
from os import environ
from django.contrib.auth.models import User
username=environ.get('DJANGO_ADMIN_USERNAME')
password=environ.get('DJANGO_ADMIN_PASSWORD')
email=environ.get('DJANGO_ADMIN_EMAIL')
User.objects.filter(email=email).delete()
User.objects.create_superuser(username, email, password)
EOF


# start the cron service
# service cron start

# install the crontab
# python manage.py crontab add

# initiate the cronjob
crond

## runserver
python manage.py runserver 0.0.0.0:9018
