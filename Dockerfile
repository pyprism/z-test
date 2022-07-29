FROM python:3.10.5-slim-bullseye

RUN apt update && apt install libjpeg62 libjpeg62-turbo-dev zlib1g-dev imagemagick -y

WORKDIR src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
