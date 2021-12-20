FROM python:3.8.12-slim-buster
LABEL maintainer="wase894@gmail.com"
EXPOSE 8080
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader all -d /usr/local/nltk_data
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 1 --timeout 240 cloudRun:app