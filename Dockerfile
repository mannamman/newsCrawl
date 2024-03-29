FROM python:3.8.12-slim-buster
LABEL maintainer="wase894@gmail.com"
ENV TRANSFORMERS_OFFLINE 1
EXPOSE 8080
WORKDIR /app
COPY . /app
RUN apt update && apt install -y curl
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader punkt -d /usr/local/nltk_data
RUN python3 -m nltk.downloader stopwords -d /usr/local/nltk_data
# 개인 스토리지
RUN curl https://storage.googleapis.com/public-model-bucket/pytorch_model_fin.bin --output /app/finBERT/models/sentiment/pytorch_model.bin
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 1 --timeout 240 main:app
