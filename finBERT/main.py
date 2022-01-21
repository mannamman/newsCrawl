from finbert.finbert import predict
from transformers import AutoModelForSequenceClassification
import os




class FinBert:
    def __init__(self):
        path = "models/sentiment"
        self.model = AutoModelForSequenceClassification.from_pretrained(path, num_labels=3,cache_dir=None)
    def pred(self, text):
        res = predict(text, self.model).to_json(orient='records')
        print(res)


if(__name__ == "__main__"):
    fin = FinBert()
    fin.pred("Inflation at 40-year high pressures consumers, Fed and Biden")