FROM bibulle/facerecognition:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL Maintainer="wisrovi.rodriguez@gmail.com"

WORKDIR /app

# install libreries for testing
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# install libreries for production
COPY src/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

RUN pip install --upgrade pip

# install libreries for production
COPY src/requirements_api.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /app

ENV PYTHONBREAKPOINT ipdb.set_trace
ENV DEBUG 1
ENV APP_ENV development

WORKDIR /app
