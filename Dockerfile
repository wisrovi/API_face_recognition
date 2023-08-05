FROM bibulle/facerecognition:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL Maintainer="wisrovi.rodriguez@gmail.com"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /app

