import json
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OllamaRequest:
  def __init__(self, uri, data):
    self.uri = uri
    self.data = data
  def __str__(self):
    return "(uri=" + self.uri + ", data=" + str(self.data) + ")"

class OllamaResponse:
  def __init__(self, response, context):
    self.response = response
    self.context = context
  def __str__(self):
    return "(response=" + self.response + ", context=" + str(self.context) + ")"

def callOllama(req):
  rawResponse = requests.post(req.uri, data=json.dumps(req.data))
  logger.debug(rawResponse.text)
  lines = rawResponse.text.splitlines()
  bits = list(map(lambda x: json.loads(x), lines))
  responsePieces = map(lambda x: x['response'], bits)
  return OllamaResponse(''.join(responsePieces), bits[-1]['context'])

def simplePayload(prompt, context=None):
  payload = {'model': 'gemma3:1b', 'prompt': prompt, 'system': '', 'options': {'temperature': 0.5, 'max_tokens': 100}}
  if (context == None):
    pass
  else:
    payload['context'] = context
  return payload

def askOllama(prompt, context=None):
  print(f">>> {prompt}")
  payload = simplePayload(prompt, context)
  req = OllamaRequest('http://localhost:8080/api/generate', payload)
  response = callOllama(req)
  print(response.response)
  return response

def main():
  r1 = askOllama('Say hello!')
  r2 = askOllama('How\'s the weather in Llamaland?', r1.context)
  r3 = askOllama('Please repeat your first response, word-for-word.', r2.context)
  r4 = askOllama('Please generate an arbitrary piece of Python code. Respond with code and only code. Do not use formatting, do not use comments. Do not wrap the code in a code block. Respond with plain text. The code should print the message of your choice and do nothing else.')
  r4stripped = r4.response.splitlines()
  r4Code = r4stripped[1:-1]
  r4Cmd = '\n'.join(r4Code)
  exec(r4Cmd)

if __name__ == '__main__':
  main()
