import requests
import os
import dotenv
import time
from jew import jwtiam 
dotenv.load_dotenv()

def cmspch():
    IAM_TOKEN = jwtiam()
    FOLDER_ID = os.environ['FOLDER_ID']
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
    file = open('uploads/speech.ogg', "rb")
    r = requests.post(f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId={FOLDER_ID}", headers=headers, data = file)
    obj = r.json()
    now = int(time.time())
    obj['date'] = now
    print(obj)
    txt = obj
    return txt