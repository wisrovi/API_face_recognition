# 1) indicamos la imagen base a usar
# https://hub.docker.com/r/bibulle/facerecognition
FROM bibulle/facerecognition

#Author and Maintainer
MAINTAINER wisrovi.rodriguez@gmail.com

# 2) creamos una carpeta para alojar los archivos del proyecto
WORKDIR /face_recognition

RUN echo face_recognition

# 3) instalamos sudo y actualizamos
#RUN apt-get update -y
#RUN apt-get -y install sudo
#RUN pip3 install --upgrade pip

# 4) instalar dependencias del SO
#RUN apt-get -y install python3-pip

# 5) instalar dependencias de python
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install cmake
RUN pip3 install dlib
RUN pip3 install face-recognition
RUN pip3 install email-validator
RUN pip3 install mysql-connector-python
RUN pip3 install Pillow
RUN pip3 install pycrypto
RUN pip3 install pycryptodome
RUN pip3 install python-dateutil
RUN pip3 install python-multipart
RUN pip3 install uvicorn
RUN pip3 install wrapt
RUN pip3 install fastapi
RUN pip3 install pydantic
#RUN pip3 install -r requirements.txt

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

# 7) le damos permisos a la carpeta donde se alojan los archivos del proyecto para que los archivos python puedan trabajar sin problemas
#RUN sudo chmod -R +777 /face_recognition

# 8) le decimos que archivo ejecutar cuando se lance el container
#CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5050" ]