FROM python:alpine3.16

RUN apk update

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip install --upgrade pip setuptools

COPY ./django/requirements.txt .

RUN pip install -r requirements.txt

COPY ./django /app

WORKDIR /app

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]