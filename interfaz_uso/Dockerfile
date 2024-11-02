# FROM python:3.10.15-alpine3.20
FROM python:3.10.15-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL Maintainer="wisrovi.rodriguez@gmail.com"

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

ENV server="api"
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# install libreries for testing
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./ /app

CMD ["python", "basic_web.py"]
