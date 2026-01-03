import logging
from ollama import ContextAwareOllama
from colors import warning

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
  ollama = ContextAwareOllama(uri='http://localhost:8080/api/generate')
  r1 = ollama.ask('Please respond to every following request with Python code and code only. Do not use formatting, do not use comments. The code should do only what was asked, and nothing else. For starters, generate a piece of code that prints simple greeting.')
  executeLLMPythonOutput(r1)
  testvar = 'This is a testvar'
  r2 = ollama.ask('Please write a piece of Python code that prints the contents of the field "testvar" of a dictionary named "env". Do not declare or define the dictionary. Assume the dictionary is already defined.')
  executeLLMPythonOutput(r2, {'testvar': testvar})

def sanitizeLLMPythonOutput(response):
  responseStripped = response.response.splitlines()[1:-1] #splits and drops the pesky markdown lines
  return '\n'.join(responseStripped)

def executeLLMPythonOutput(response, env = {}):
  cmd = sanitizeLLMPythonOutput(response)
  logger.warning(warning(f"Attempting to execute {cmd}."))
  exec(cmd)

if __name__ == '__main__':
  main()
