from modules.req_valid import auth_deco, health_cors
from modules.log_module import Logger
from finBERT.sentiment import FinBert
import json
import traceback
from flask import Request, Response
import requests

# 객체 초기화(공통으로 사용되는)
sentiment_finbert = None
logger = Logger()


def init_sentiment():
    global sentiment_finbert
    sentiment_finbert = FinBert()

@health_cors
@auth_deco
def index(request: Request):
    global logger
    global sentiment_finbert

    # lazy loading
    if(sentiment_finbert is None):
        init_sentiment()

    try:
        # post 메시지 파싱
        recevied_msg = json.loads(request.get_data().decode("utf-8"))
        input_url = recevied_msg["input_url"][0]
        header = recevied_msg["header"][0]
        upload_url = recevied_msg["upload_url"][0]

        res = requests.get(input_url)
        context = res.content.decode("utf-8")
        if(res.status_code != 200):
            return Response(response=context, status=res.status_code)

        sentenses = context.split("\n") 
        sentenses = [sentense.strip() for sentense in sentenses]

        results = list()

        for sentense in sentenses:
            results.append(sentiment_finbert.pred(sentense))

        res = requests.put(upload_url, data=json.dumps(results).encode("utf-8"), headers=header)
        
        return Response(response=res.content.decode("utf-8"), status=res.status_code)

    except Exception:
        error = traceback.format_exc()
        logger.error_log(error)
        return Response(response=error, status=400)
    