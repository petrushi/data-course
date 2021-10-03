import requests
import json
import os
from dotenv import load_dotenv

# https://developers.google.com/youtube/registering_an_application - инструкция для получения API ключа

load_dotenv(dotenv_path='../.env')  # загружаю переменные окружения из файла .env в корневой папке курса
API_KEY = os.environ['YT_API_KEY']
USERNAME = 'WolframResearch'

channel_info = requests.get(f'https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&forUsername={USERNAME}')

with open('task_2.json', 'w') as f:
    json.dump(channel_info.json(), f)
