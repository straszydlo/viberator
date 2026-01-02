import logging
from ollama import Ollama

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
  ollama = Ollama(uri='http://localhost:8080/api/generate')
  r1 = ollama.ask('Say hello!')
  r2 = ollama.ask('How\'s the weather in Llamaland?', r1.context)
  r3 = ollama.ask('Please repeat your first response, word-for-word.', r2.context)
  r4 = ollama.ask('Please generate an arbitrary piece of Python code. Respond with code and only code. Do not use formatting, do not use comments. Do not wrap the code in a code block. Respond with plain text. The code should print the message of your choice and do nothing else.', r3.context)
  r4Cmd = sanitizeLLMPythonOutput(r4.response)
  logger.warning(f"Attempting to execute {r4Cmd}.")
  exec(r4Cmd)

def sanitizeLLMPythonOutput(response):
  responseStripped = response.splitlines()[1:-1] #splits and drops the pesky markdown lines
  return '\n'.join(responseStripped)

if __name__ == '__main__':
  main()
