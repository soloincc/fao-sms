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


Service Providers
------------
**Africastalking and Nexmo were implemented in the app.** Setting up of the account for Infobip took long due to their KYC (Know Your Customer) procedures which wasn't complete during the 48 hour window of this task


My approach to the test
------------

The app is developed using python3 and the Django framework. It uses MySQL as the database and has a provision of using Redis for queueing high volumes of messages. The app has been dockerized.
```bash
version: '3.7'
services:
  db:
    build:
      context: .
      dockerfile: ./docker/db-Dockerfile
    restart: unless-stopped
    env_file:
      - 'variables.env'
    volumes:
      - ./db_data:/var/lib/mysql:rw
    ports:
      - target: 3306
        protocol: tcp

    networks:
      - sms-network

  # app
  sms-app:
    restart: unless-stopped
    build:
      context: .
    command: bash -c "./docker/wait-for-it.sh db:3306 --timeout=600 --strict -- ./docker/docker-entrypoint.sh"
    env_file:
      - 'variables.env'
    networks:
      - sms-network
    ports:
      - 9018:9018
    links:
      - db

  # redis
  redis:
    restart: unless-stopped
    image: redis
    ports:
      - 6381:6379
    networks:
      - sms-network

#Docker Networks
networks:
  sms-network:
    driver: bridge
```

### The messages are stored in a queue ready to be dispatched
A table was created to store this queue
```bash
+---------------+---------------+------+-----+---------+----------------+
| Field         | Type          | Null | Key | Default | Extra          |
+---------------+---------------+------+-----+---------+----------------+
| id            | int(11)       | NO   | PRI | NULL    | auto_increment |
| date_created  | datetime      | NO   |     | NULL    |                |
| date_modified | datetime      | NO   |     | NULL    |                |
| message       | varchar(1000) | NO   |     | NULL    |                |
| recepient_no  | varchar(15)   | NO   |     | NULL    |                |
| msg_status    | varchar(50)   | NO   |     | NULL    |                |
| schedule_time | datetime      | NO   |     | NULL    |                |
| in_queue      | tinyint(1)    | NO   |     | NULL    |                |
| queue_time    | datetime      | YES  |     | NULL    |                |
| delivery_time | datetime      | YES  |     | NULL    |                |
| recepient_id  | int(11)       | NO   | MUL | NULL    |                |
| template_id   | int(11)       | NO   | MUL | NULL    |                |
| provider_id   | varchar(100)  | YES  |     | NULL    |                |
+---------------+---------------+------+-----+---------+----------------+
```

In addition an automatic script was developed to automatically populate this table and other relative tables. This script is executed by running `python manage.py add_test_data sms_app/input_sms.csv`


### The messages are valid for 48 hours and within/after this period each message should have a uniquely identifiable status independent of the service provider
A message status field was added to the table. This field is populated with the message status at any given time. Some of this status include, *SCHEDULED*, *QUEUED*, *SENT*, *DELIVERED* and other operator statuses depending on the state of the message


### The messages might be grouped into campaigns where one, two or more of them are sent to multiple recipients
Campaign and message template tables were created. The campaign table holds a list of campaigns, while the message templates table contains messages which might be sent in a campaign. The message template table design caters for message templates which might not necessarily be sent in a campaign. When a campaign is ran, the sms queue is populated with messages from the template as well as the data from the recepients table.

**Campaign table**
```bash
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| date_created  | datetime     | NO   |     | NULL    |                |
| date_modified | datetime     | NO   |     | NULL    |                |
| campaign_name | varchar(100) | NO   | UNI | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
```

**Message template table**
```bash
+---------------+---------------+------+-----+---------+----------------+
| Field         | Type          | Null | Key | Default | Extra          |
+---------------+---------------+------+-----+---------+----------------+
| id            | int(11)       | NO   | PRI | NULL    | auto_increment |
| date_created  | datetime      | NO   |     | NULL    |                |
| date_modified | datetime      | NO   |     | NULL    |                |
| template      | varchar(5000) | NO   |     | NULL    |                |
| uuid          | varchar(36)   | NO   | UNI | NULL    |                |
| campaign_id   | int(11)       | YES  | MUL | NULL    |                |
+---------------+---------------+------+-----+---------+----------------+
```


### The messages might be longer than the maximum allowed length of 918 characters
The app holds the full length of the message in the message template. The message is only broken down into parts when being added to the SMS queue. The maximum allowed length is a setting which is set in the settings


### All service providers provide HTTP endpoints and you should wrap the providers' API
This is implemented by using the documentation from the service providers

### The service should be able to reliably switch providers during run-time without losing messages
The app can randomly choose the service provider during runtime without losing messages. This is demonstrated by manually running the send messages command without giving a default provider `python manage.py send_scheduled_sms`

**NOTE**: I called for some further clarification on this feature, but unfortunately I didn't get the technical person

### Developers should be able to use new providers without the need to extend or modify the service
Done. Additional providers can easily be added 


### The service may be organized into a class, module or both.
The app is organised in both




Functionality
------------

The app supports sending messages via Africastalking and Nexmo. The process of setting an account at infobib took more time than was allocated for the task

For each of the configured gateway, callback endpoints have been defined. The SMS gateways will automatically call the endpoints with the delivery reports

The app automatically collects runtime errors and submits them to a [Sentry instance hosted by Badili](https://sentry.badili.co.ke)

## Caveats

When sending the messages via Nexmo, the numbers must be whitelisted. Only 3 numbers have been listed, 254726xxxxx97, 254733xxxxx97, 254715xxxxx04