import requests
import json

username = 'petrochenkov'
repos = requests.get(f'https://api.github.com/users/{username}/repos')

with open('task_1.json', 'w') as f:
    json.dump(repos.json(), f)
