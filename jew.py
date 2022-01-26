import time
import jwt
import requests
import os


service_account_id = os.environ['ACC_ID']
key_id = os.environ['KEY_ID'] # ID ресурса Key, который принадлежит сервисному аккаунту.
token_ttl = 3600

with open("private.pem", 'r') as private:
  private_key = private.read() # Чтение закрытого ключа из файла.

token = ""
last_update = 0

def jwtiam():
    global token, last_update
    now = int(time.time())
    if now-last_update <= token_ttl-10:
      return token
    payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': service_account_id,
            'iat': now,
            'exp': now + token_ttl}

    # Формирование JWT.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id})

    et = str(encoded_token.decode('utf8'))
    r = requests.post("https://iam.api.cloud.yandex.net/iam/v1/tokens", json={"jwt": et})
    obj = r.json()
    iamt = obj["iamToken"]
    token = iamt
    last_update = now
    print(token)
    return token
