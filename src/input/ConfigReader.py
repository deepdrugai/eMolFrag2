
from eMolFrag2.src.utilities import logging, constants
from pathlib import Path

def cleanCommandList(cmdList):
  """
      Trims whitespace and other discrepancies
      
      @output: a list of flags and arguments
  """
  retList = []
  bad_tokens = ["", " ", "\n"]
  for token in cmdList:
    if token not in bad_tokens:
      retList.append(token)

  return retList
    
def grabCommands(config_file):
  """
      Takes the string contents of a configuration file
      and grabs its command line arguments.
      If there are comments, ignore anything to the right of it
      
      @output: a list of flags and arguments
  """
  retString = ""
  position = 0

  with open (config_file) as f:
    contents = f.readlines()

  #Read line by line, ignore comments, concatenate the remaining tokens into one string
  for line in contents:
      position = line.find("#")
      if (position >= 0):
          retString += line[:position]
      else:
          retString += line

  if (len(retString) <= 0):
    logging.logger.error(f"Configuration File is empty")
    return None

  return cleanCommandList(retString.split(" "))

def readConfig(config_file, parser):
  """
      Reads a config file and parses arguments
      If the file is empty, throw an error
      
      @output: parsed arguments from argparser
  """
  if not Path(config_file).exists():
    logging.logger.error(f"{Path(config_file)} does not exist")
    return None

  if Path(config_file).suffix != constants.EMF_FORMAT_EXT:
    logging.logger.error(f"Configuration files must have the {constants.EMF_FORMAT_EXT} extension")
    return None

  #Grab the commands and then parse them
  cmdList = grabCommands(config_file)

  args = parser.parse_args(cmdList)
  if args.i is None or args.o is None:
    logging.logger.error(f'Command-line arguments failed to parse; execution of eMolFrag will stop.')
    return None

  return args