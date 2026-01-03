# stolen from https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py

class Colors:
  LLMOUTPUT = '\033[95m'
  PROMPT = '\033[94m'
  WARNING = '\033[93m'
  ENDC = '\033[0m'

def warning(string):
  return __prefix(Colors.WARNING, string)
 
def prompt(string):
  return __prefix(Colors.PROMPT, string)

def llmOutput(string):
  return __prefix(Colors.LLMOUTPUT, string)

def __prefix(prefix, string):
  return f"{prefix}{string}{Colors.ENDC}"
