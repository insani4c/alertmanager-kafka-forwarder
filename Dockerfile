# syntax=docker/dockerfile:1

FROM python:3.11-alpine

LABEL maintainer="Johnny Morano <daimyo@shihai-corp.com>"

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/app.py .

RUN pip3 install -r requirements.txt

EXPOSE 9792

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9792"]
