import time
import jwt
import requests

service_account_id = "ajevquifrhs1lfrcfsas"
key_id = "ajeuep7grfuk9o8e2vid" # ID ресурса Key, который принадлежит сервисному аккаунту.
token_ttl = 600

with open("private.pem", 'r') as private:
  private_key = private.read() # Чтение закрытого ключа из файла.

def jwtiam():
    now = int(time.time())
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
    return iamt

print(jwtiam())
