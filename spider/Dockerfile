FROM python:3.8-buster
WORKDIR /app
RUN  mkdir /app/utils
COPY * /app
COPY utils/*  /app/utils 
RUN pip3 install -r /app/requirements.txt

