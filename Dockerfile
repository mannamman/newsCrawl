FROM python:3.8.12-slim-buster
LABEL maintainer="wase894@gmail.com"
ENV TRANSFORMERS_OFFLINE 1 
EXPOSE 8080
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader punkt -d /usr/local/nltk_data
RUN python3 -m nltk.downloader stopwords -d /usr/local/nltk_data
# finbert
RUN gdown https://drive.google.com/uc?id=1frgtv2KYvoega8IrL4PGlA8lAO_dh9If -O /app/finBERT/models/sentiment/pytorch_model.bin
# CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 1 --timeout 240 main:app