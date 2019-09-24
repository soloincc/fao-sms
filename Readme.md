Wangoru Kihara - FAO SMS developer written test
============================

A Wangoru Kihara implementation of the FAO written test for the SMS developer position

Building and Running using docker
------------

The app has been dockerized

You need to install docker in your machine. Follow the [installation steps for your environment](https://docs.docker.com/install/)

Clone the application `git clone https://gitlab.com/soloincc/fao-sms`

The app has scheduled some default SMS to be sent when the app is built while others have been scheduled for a future date. The SMS are defined in the csv file `sms_app/input_sms.csv` You can edit this file appropriately before building and running


Build and ran the application
```bash
cd fao-sms
docker-compose build
docker-compose up
```

Building and Running using virtual environment
------------

The app uses python3. Follow the [installation steps for your environment](https://realpython.com/installing-python/)

Clone the application, instantiate a virtual, install the requirements and ran the application
```bash
cd /tmp/
git clone https://gitlab.com/soloincc/fao-sms
cd /tmp/fao-sms
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Manually running the app
------------

The app contain endpoints that can be ran manually when the application is already initiated
```bash
# To add the predefined SMS to the SMS queue
# The input sms can be subsituted by any csv that contains the first line as header
# The csv should have the columns message, recepient_nos, campaign, sending_time
# Each row after the header represents a SMS to be queued.
# The app automatically creates the campaign and recepients if they are not defined in the database
# The sending time for the messages can be left blank and it will be set as the time the script is ran
# The sending time can also be initiated as now, yesterday, tomorrow or today and the appropriate timestamps will be calculated
# The recepient field may contain one or many recepients phone numbers. In case of many recepients, the phone numbers must be comma separated
# The phone numbers must begin with a plus(+) sign for each phone number
python manage.py add_test_data sms_app/input_sms.csv

# Send queued messages to the SMS gateways
# The queued messages can be sent to the configured SMS gateways
# Either provide the provider to use or leave blank for the app to determine the appropriate gateway to use
# The configured gateways are at and nexmo for Africastalking and Nexmo respectively
python manage.py send_scheduled_sms --provider nexmo

# OR

python manage.py send_scheduled_sms

```

Functionality
------------

The app supports sending messages via Africastalking and Nexmo. The process of setting an account at infobib took more time than was allocated for the task

For each of the configured gateway, callback endpoints have been defined. The SMS gateways will automatically call the endpoints with the delivery reports

The app automatically collects runtime errors and submits them to a [Sentry instance hosted by Badili](https://sentry.badili.co.ke)

## Caveats

When sending the messages via Nexmo, the numbers must be whitelisted. Only 3 numbers have been listed, 254726xxxxx97, 254733xxxxx97, 254715xxxxx04