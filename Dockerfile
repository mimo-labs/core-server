FROM python:3-alpine

LABEL maintainer="Lucio Delelis <ldelelis@est.frba.utn.edu.ar>"

RUN mkdir /www
WORKDIR /www
COPY requirements.txt /www/

ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . /www/
WORKDIR mockserver

EXPOSE 12021/tcp

