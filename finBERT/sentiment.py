from finBERT.finbert.finbert import predict
from transformers import AutoModelForSequenceClassification
import os
import json




class FinBert:
    def __init__(self):
        # 실행한 디렉토리 기준으로 상대경로를 입력
        self.path = "finBERT/models/sentiment"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.path, num_labels=3,cache_dir=None)
        self.labels = ["positive", "negative", "neutral"]

    def _make_dic(self, text, logit):
        return_dic = {
            "sentence" : text,
        }
        for label, val in zip(self.labels, logit):
            return_dic[label] = val
        return return_dic

    def pred(self, text):
        res = json.loads(predict(text, self.model, self.path).to_json(orient='records'))[0]
        return self._make_dic(text, res["logit"])


if(__name__ == "__main__"):
    fin = FinBert()
    fin.pred("Inflation at 40-year high pressures consumers, Fed and Biden")