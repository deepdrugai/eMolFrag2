import sys
from pathlib import Path
from SuperSecretProject.src.utilities import logging
from SuperSecretProject.src.input import Options

usr_dir = Path.cwd()
dataPath = usr_dir.joinpath("SuperSecretProject/unittests/data/db-files")
mol2 = dataPath.joinpath("mol2")
smi = dataPath.joinpath("smi")
sdf = dataPath.joinpath("sdf")
pdb = dataPath.joinpath("pbd")
mol = dataPath.joinpath("mol")

def runOptions(test_file):
  sys.argv = ['/content/SuperSecretProject/src/eMolFrag.py','-i', str(test_file), '-o', '/content/output']
  options = Options.Options()
  assert options.isRunnable()

def runOptionsByFolder(folder):
  for current_file in folder.iterdir():
    runOptions(current_file)

def runOptionsTests():
  folders = [mol2, smi, pdb, mol]
  for folder in folders:
    runOptionsByFolder(folder)

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
    tests = {"runOptions": runOptionsTests}

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