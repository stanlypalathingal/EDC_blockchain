#!/bin/bash

LABEL maintainer="stanlywilson@stvincentngp.edu.in"

# for ubuntu based system
FROM python:3.7-slim-buster
RUN apt-get -q update && \ apt-get -qy install \ gcc

# for Raspberry Pi
#FROM arm32v7/python:3.7-slim-buster
#RUN apt-get -q update && \ apt-get -qy install \ libatlas-base-dev \ libgomp1

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --extra-index-url=https://piwheels.org/simple -r requirements.txt 

ADD . /

ENTRYPOINT ["python3","EDC_x.py"]
