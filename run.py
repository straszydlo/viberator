import json
import requests

payload = {'model': 'gemma3:1b', 'prompt': 'Say hello!', 'system': '', 'options': {'temperature': 0.5, 'max_tokens': 100}}

response = requests.post("http://localhost:8080/api/generate", data=json.dumps(payload))
lines = response.text.splitlines()
bits = list(map(lambda x: json.loads(x), lines))
pieces = list(map(lambda x: x['response'], bits))

print(''.join(pieces))
