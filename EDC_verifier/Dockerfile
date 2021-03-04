#!/bin/bash
FROM arm32v7/python:3.7-slim-buster

RUN apt-get -q update && \
	apt-get -qy install \ 
	libatlas-base-dev \
	libgomp1

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -r requirements.txt 
# RUN pip install "pymongo" --no-cache-dir --extra-index-url=https://www.piwheels.org/simple
ADD . /



ENTRYPOINT ["python3","EDC_verifier.py"]


