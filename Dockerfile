FROM python:3.9-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get -y install gcc g++ libgeos++-dev libgeos-c1v5 libgeos-dev libgeos-doc libgdal-dev

RUN pip3 install -r requirments.txt

EXPOSE 8000

CMD ['uvicorn', 'basic_code.main:app', '--host 0.0.0.0', '--port 8000']