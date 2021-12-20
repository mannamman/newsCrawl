FROM python:3.8.12-slim-buster
LABEL maintainer="wase894@gmail.com"
EXPOSE 8080
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN [ "python3", "-c", "import nltk; nltk.download('stopwords'); nltk.download('punkt')" ]
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 1 --timeout 240 cloudRun:app