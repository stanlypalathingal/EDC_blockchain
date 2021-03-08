#!/bin/bash

#FROM arm32v7/python:3.7-slim-buster
FROM python:3.7-slim-buster

LABEL maintainer="stanlywilson@stvincentngp.edu.in"

RUN apt-get -q update && \
	apt-get -qy install \ 
	gcc

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --extra-index-url=https://piwheels.org/simple -r requirements.txt 

ADD . /

ENTRYPOINT ["python3","EDC_x.py"]

