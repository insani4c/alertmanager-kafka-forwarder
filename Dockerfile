# syntax=docker/dockerfile:1

FROM python:3.12-alpine
ENV LIBRD_VER="2.1.0"

LABEL maintainer="Johnny Morano <daimyo@shihai-corp.com>"

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src/app.py .

RUN sed -i -e 's/v3\.[0-9]\+/edge/g' /etc/apk/repositories \
    && apk upgrade --update-cache --available

RUN apk add --no-cache --virtual .make-deps unzip bash make wget git gcc g++ \
    && apk add --no-cache musl-dev zlib-dev openssl zstd-dev pkgconfig libc-dev \
    && wget https://github.com/confluentinc/librdkafka/archive/refs/tags/v${LIBRD_VER}.tar.gz \
    && tar -xvf v${LIBRD_VER}.tar.gz \
    && cd librdkafka-${LIBRD_VER} \
    && ./configure --prefix /usr \
    && make && make install && make clean \
    && cd .. \
    && rm -rf librdkafka-${LIBRD_VER} \
    && rm -rf v${LIBRD_VER}.tar.gz

RUN pip3 install -r requirements.txt
RUN apk del .make-deps && rm -rf /var/cache/apk/*

EXPOSE 9792

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9792"]
