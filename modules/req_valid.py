import functools
from flask import Response, Request
import os

def health_cors(func):
    @functools.wraps(func)
    def wrapper(req: Request):
        if(req.method == "GET"):
            return Response(status=200, response="pong")
        elif(req.method == 'OPTIONS'):
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': ["GET","POST"],
                'Access-Control-Allow-Headers': ['Content-Type', 'Authorization'],
                'Access-Control-Max-Age': '3600'
            }
            return Response(status=204, response="", headers=headers)
        return func(req)
    return wrapper


def auth_deco(func):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    @functools.wraps(func)
    def valid(req: Request):
        if("Authorization" not in req.headers):
            return Response(status=401, response="Authorization is not exist", headers=headers)
        # 헤더 분리
        api_key_header = req.headers["Authorization"]
        try:
            # bearer, key 분리
            key_type, req_api_key = api_key_header.split(" ")
            if(key_type.lower() != "bearer"):
                raise ValueError
            # 암호 불러오기
            env_api_key = os.environ.get("api_key", None)
            # 검사
            if(req_api_key != env_api_key):
                raise ValueError
        except ValueError:
            return Response(status=401, response="Authorization is not correct format", headers=headers)
        return func(req)
    return valid