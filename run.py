import logging
import tkinter as tk
from ollama import ContextAwareOllama
from colors import warning

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ollama = ContextAwareOllama(uri = 'http://localhost:8080/api/generate')

def main():
  r1 = ollama.ask('Please respond to every following request with Python code and code only. Do not use formatting, do not use comments. The code should do only what was asked, and nothing else. For starters, generate a piece of code that prints a message indicating that an app named "Viberator 9000" is now running and fully operational.')
  executeLLMPythonOutput(r1)
  root = tk.Tk()
  root.title('Viberator 9000')
  canvas = tk.Canvas(root, width = 800, height = 600, bg = 'white')
  canvas.pack(anchor = tk.CENTER, expand = True)
  r2 = ollama.ask('Generate code that calls a Tkinter method on a variable named "canvas" that creates a green rectangle on that canvas.')
  executeLLMPythonOutput(r2, env = { 'canvas': canvas })
  root.bind("<KeyPress>", keyPressed(canvas, ollama))
  root.bind("<Escape>", escapePressed(ollama))
  root.geometry('800x600')
  root.mainloop()

def keyPressed(canvas, ollama):
  return lambda event: askOllamaForCircle(event, canvas, ollama)

def askOllamaForCircle(event, canvas, ollama):
  response = ollama.ask(f"A Tkinter event {event} was registered. Generate code that calls a Tkinter method on a variable named \"canvas\" that creates a red circle on that canvas at the x and y coordinates from the event.")
  executeLLMPythonOutput(response, env = { 'canvas': canvas })

def escapePressed(ollama):
  return lambda event: runEscape(ollama, event)

def runEscape(ollama, event):
  print(event)
  response = ollama.ask('Please generate a line of Python code that exits the app immediately.')
  executeLLMPythonOutput(response)

def sanitizeLLMPythonOutput(response):
  responseStripped = response.response.splitlines()[1:-1] #splits and drops the pesky markdown lines
  return '\n'.join(responseStripped)

def executeLLMPythonOutput(response, env = {}):
  cmd = sanitizeLLMPythonOutput(response)
  logger.warning(warning(f"Attempting to execute {cmd}."))
  exec(cmd, env)

if __name__ == '__main__':
  main()
