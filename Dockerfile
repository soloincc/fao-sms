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

# create the folder where the static files will be collected to
# RUN mkdir /opt/aagris/static

# Copy the requirements file and install the requirements
COPY requirements.txt /opt/fao_sms/
RUN pip install -r /opt/fao_sms/requirements.txt

# Change to the static dir and install the npm packages
# WORKDIR /opt/aagris_static
# COPY aagris/static/package.json .
# RUN npm install

# we need to install d3-slider on its own
# WORKDIR /opt/aagris_static/node_modules

# Enter the the base folder
WORKDIR /opt/fao_sms

# add (the rest of) our code
ADD . /opt/fao_sms/

CMD ["/opt/fao_sms/docker/docker-entrypoint.sh"]
