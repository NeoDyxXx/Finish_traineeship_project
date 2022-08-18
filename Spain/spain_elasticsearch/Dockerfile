FROM python:3.9.11

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install flask
RUN pip install bs4
RUN pip install connexion
RUN pip install lxml
RUN pip install flask_swagger_ui

CMD ["python", "app.py"]