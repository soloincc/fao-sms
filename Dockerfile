FROM python:3.7-alpine3.9

MAINTAINER Wangoru Kihara wangoru.kihara@badili.co.ke

RUN apk add mysql-dev ca-certificates \
    mysql-client \
    python3-dev \
    git \
    curl \
    wget \
    jpeg-dev zlib-dev \
    gcc libc-dev g++ \
    bash \
    coreutils

## default variables
ARG APP_DIR=/opt/fao_sms

# Create our base folder
RUN mkdir /opt/fao_sms

# Copy the requirements file and install the requirements
COPY requirements.txt /opt/fao_sms/
RUN pip install -r /opt/fao_sms/requirements.txt

# Enter the the base folder
WORKDIR /opt/fao_sms

# add (the rest of) our code
ADD . /opt/fao_sms/

# move the variables.env file
COPY variables.env /opt/fao_sms/sms_app/.env

# use the EAT timezone
RUN apk update && apk add tzdata
# COPY /usr/share/zoneinfo/Africa/Nairobi /etc/localtime
RUN echo "Africa/Nairobi" > /etc/timezone
ENV TZ=Africa/Nairobi

CMD ["/opt/fao_sms/docker/docker-entrypoint.sh"]
