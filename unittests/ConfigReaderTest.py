import sys
from pathlib import Path
from eMolFrag2.unittests import utilities
from eMolFrag2.src.utilities import logging
from eMolFrag2.src.input import ConfigReader

usr_dir = Path.cwd()
config_files = usr_dir.joinpath("eMolFrag2/unittests/data/configuration-files")

def runReadNormalConfig(config_file):
  parser = utilities.createParser()
  args = ConfigReader.readConfig(config_file, parser)
  assert args.i is not None and args.o is not None

def runReadNullConfig(config_file):
  parser = utilities.createParser()
  args = ConfigReader.readConfig(config_file, parser)
  assert args is None

def runReadConfigTests():
  #normal
  runReadNormalConfig(config_files.joinpath("comment1.emf"))
  runReadNormalConfig(config_files.joinpath("comment3.emf"))
  runReadNormalConfig(config_files.joinpath("comment4.emf"))
  runReadNormalConfig(config_files.joinpath("normal1.emf"))

  #empty
  runReadNullConfig(config_files.joinpath("empty.emf"))
  runReadNullConfig(config_files.joinpath("comment2.emf"))

  #missing arguments
  runReadNullConfig(config_files.joinpath("missinginput.emf"))
  runReadNullConfig(config_files.joinpath("missingoutput.emf"))

  #wrong file type
  runReadNullConfig(config_files.joinpath("wrongextension.txt"))

  #file does not exist
  runReadNullConfig(config_files.joinpath("madeup.emf"))



#
#
# Unit test initiation functionality
#
#
def runtest1(func):

    try:
       func()
       return True

    except:
       return False


def runtest(test_name, test_func, successful, failed):
    if runtest1(test_func):
        successful.append(test_name)
    else:
        failed.append(test_name)

def runtests():
    printlevel = 1
    logging.logger.info(f"Executing {__name__} unit tests.")
    
    #
    # Define all tests as a Dictionary: {str-name, <function-to-execute>}
    #
    tests = {"readConfig": runReadConfigTests}

    #
    # Run
    #
    successful = []
    failed = []
    for test_name, test_func in tests.items():
        runtest(test_name, test_func, successful, failed)

    # 
    # Report
    #
    if not failed:        
        logging.logger.info(f'{__name__} unit tests are successful.')

    else:
        for test in failed:
            logging.logger.error(f'Failed {test}.')

if __name__ == "__main__":
    runtests()