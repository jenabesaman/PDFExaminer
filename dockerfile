FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3 python3-pip php

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8536

CMD ["python3", "app.py"]