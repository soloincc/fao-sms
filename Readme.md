Wangoru Kihara - FAO SMS developer written test
============================

A Wangoru Kihara implementation of the FAO written test for the SMS developer position

## Building and Running
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

## Functionality

The app supports sending messages via Africastalking and Nexmo. The process of setting an account at infobib took more time than was allocated for the task

## Caveats

When sending the messages via Nexmo, the numbers must be whitelisted. Only 3 numbers have been listed, 254726xxxxx97, 254733xxxxx97, 254715xxxxx04