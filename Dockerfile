# syntax=docker/dockerfile:1

FROM python:3.11-alpine

LABEL maintainer="Johnny Morano <daimyo@shihai-corp.com>"

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/app.py .

RUN sed -i -e 's/v3\.[0-9]\+/edge/g' /etc/apk/repositories \
    && apk upgrade --update-cache --available 
    
RUN apk add --no-cache librdkafka librdkafka-dev gcc g++ && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements.txt
RUN apk del gcc g++ librdkafka-dev && rm -rf /var/cache/apk/*

EXPOSE 9792

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9792"]
