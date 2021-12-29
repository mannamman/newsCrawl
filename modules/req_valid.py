import functools
from flask import Response
import os
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP


def health_cors(func):
    @functools.wraps(func)
    def wrapper(req):
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
    def valid(req):
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
            private_key_str = os.environ.get('private', None).encode("utf-8")
            secret = os.environ.get("secret", None).encode("utf-8")
            env_api_key = os.environ.get("api_key", None)

            # 비공개 키 로드
            padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            private_key = load_pem_private_key(private_key_str, password=secret)

            # 복호화
            decrypted = private_key.decrypt(req_api_key, padding).decode("utf-8")
            # 검사
            if(decrypted != env_api_key):
                raise ValueError
        except ValueError:
            return Response(status=401, response="Authorization is not correct format", headers=headers)
        return func(req)
    return valid