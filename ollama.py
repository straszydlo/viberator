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

class Ollama:
  def __init__(self, uri):
    self.uri = uri

  def __call(self, req):
    rawResponse = requests.post(req.uri, data=json.dumps(req.data))
    logger.debug(rawResponse.text)
    lines = rawResponse.text.splitlines()
    bits = list(map(lambda x: json.loads(x), lines))
    responsePieces = map(lambda x: x['response'], bits)
    return OllamaResponse(''.join(responsePieces), bits[-1]['context'])
  
  def __simplePayload(self, prompt, context=None):
    payload = {'model': 'gemma3:1b', 'prompt': prompt, 'system': '', 'options': {'temperature': 0.5, 'max_tokens': 100}}
    if (context == None):
      pass
    else:
      payload['context'] = context
    return payload

  def ask(self, prompt, context=None):
    print(f">>> {prompt}")
    payload = self.__simplePayload(prompt, context)
    req = OllamaRequest(self.uri, payload)
    response = self.__call(req)
    print(response.response)
    return response

