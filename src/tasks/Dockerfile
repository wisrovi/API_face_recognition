FROM bibulle/facerecognition:latest

ENV PYTHONUNBUFFERED 1

MAINTAINER wisrovi.rodriguez@gmail.com

WORKDIR /app

RUN pip3 install redis
RUN pip3 install celery

COPY ../tasks /app

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info", "--pool=solo"]
