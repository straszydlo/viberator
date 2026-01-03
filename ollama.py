import colors
import json
import logging
import requests
import textwrap

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OllamaRequest:
  def __init__(self, data):
    self.data = data
  def __str__(self):
    return "(data=" + str(self.data) + ")"

class OllamaResponse:
  def __init__(self, response, context):
    self.response = response
    self.context = context
  def __str__(self):
    return "(response=" + self.response + ", context=" + str(self.context) + ")"

class Ollama:
  def __init__(self, uri):
    self.uri = uri

  def _call(self, req):
    rawResponse = requests.post(self.uri, data=json.dumps(req.data))
    logger.debug(rawResponse.text)
    lines = rawResponse.text.splitlines()
    bits = list(map(lambda x: json.loads(x), lines))
    responsePieces = map(lambda x: x['response'], bits)
    return OllamaResponse(''.join(responsePieces), bits[-1]['context'])
  
  def _simplePayload(self, prompt, context=None):
    payload = {'model': 'gemma3:1b', 'prompt': prompt, 'system': '', 'options': {'temperature': 0.3, 'max_tokens': 300}}
    if (context == None):
      pass
    else:
      payload['context'] = context
    return payload

  def ask(self, prompt, context=None):
    print(colors.prompt(f">>> {prompt}"))
    payload = self._simplePayload(prompt, context)
    req = OllamaRequest(payload)
    response = self._call(req)
    print(colors.llmOutput("<<<\n" + textwrap.indent(f" {response.response}", '  ')))
    return response

class ContextAwareOllama(Ollama):
  def __init__(self, uri):
    super().__init__(uri)
    self.context = None

  def ask(self, prompt):
    response = super().ask(prompt, context=self.context)
    self.context = response.context
    return response
