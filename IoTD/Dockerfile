#!/bin/bash

#FROM arm32v7/python:3.7-slim-buster
FROM python:3.7-slim-buster

LABEL maintainer="stanlywilson@stvincentngp.edu.in"

RUN apt-get -q update && \
	apt-get -qy install \ 
	gcc

#COPY requirements.txt ./requirements.txt
#RUN pip3 install --no-cache-dir --extra-index-url=https://piwheels.org/simple -r requirements.txt 
#RUN pip3 install --no-cache-dir -r requirements.txt 

RUN pip3 install --no-cache-dir "pandas==0.25.3" 
RUN pip3 install --no-cache-dir "paho-mqtt"
RUN pip3 install --no-cache-dir "pycrypto==2.6.1"

ADD . /


ENTRYPOINT ["python3","iotd_data_generators.py"]

