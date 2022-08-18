FROM python:3.10

WORKDIR /app

COPY . /app

RUN ./create_env.sh

EXPOSE 8000

ENTRYPOINT [ "python" ]
CMD [ "run.py"]
