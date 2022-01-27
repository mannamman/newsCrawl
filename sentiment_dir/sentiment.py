from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

import numpy as np
from scipy.special import softmax
import os

class NewsSentiment:
    def __init__(self):
        path = f"{os.getcwd()}/sentiment_dir"
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.labels = ['negative', 'neutral', 'positive']
        self.model = AutoModelForSequenceClassification.from_pretrained(path)


    def _pred(self, text :str) -> dict:
        result_dict = {
            "input_text" : text
        }
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        return self._result_rank(scores, result_dict)

    def _result_rank(self, scores, result_dict :dict) -> dict:
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = self.labels[ranking[i]]
            s = scores[ranking[i]]
            result_dict[l] = float(np.round(float(s), 4))
        return result_dict

    def pred(self, text :str):
        result = self._pred(text)
        return result

if(__name__ == "__main__"):
    test = NewsSentiment()
    text = "Inflation at 40-year high pressures consumers, Fed and Biden"
    print(test.pred(text))