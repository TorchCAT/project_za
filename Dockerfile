# FROM ubuntu:18.04
# RUN apt-get update
# RUN apt-get install -y python3.8 python3-pip
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8

FROM python:3.8-slim-buster
WORKDIR /app
RUN mkdir uploads
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP="main.py"
CMD flask run --host=0.0.0.0
