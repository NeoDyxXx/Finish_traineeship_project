FROM python:3.9

WORKDIR /usr/lithuania-api

COPY requirements.txt  .
RUN pip install -r requirements.txt

COPY flask_app flask_app
EXPOSE 5000

CMD ["python", "./flask_app/lithuania_scraper_embassy/union_embassy_data.py"]
CMD ["python", "./flask_app/lithuania_scraper/union_centre_data.py"]
CMD ["python", "./flask_app/app.py"]
