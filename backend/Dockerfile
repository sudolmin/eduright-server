FROM python:alpine3.16

RUN apt update
RUN pip install --upgrade pip
RUN apt-get install ffmpeg curl libsm6 libxext6 \
    libpq-dev cmake gcc python3-dev musl-dev -y \
    && pip install psycopg2

COPY ./django/requirements.txt .

RUN pip install -r requirements.txt
RUN pip install docker

COPY ./django /app

WORKDIR /app

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]