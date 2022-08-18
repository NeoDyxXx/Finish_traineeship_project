FROM ubuntu:latest
RUN apt-get update -y &&\
    apt-get install -y python3-pip python-dev build-essential

ADD . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python3 app.py
