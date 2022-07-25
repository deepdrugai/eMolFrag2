import sys
from pathlib import Path
from eMolFrag2.src.utilities import logging
from eMolFrag2.src.input import Options, MoleculeFileReader

usr_dir = Path.cwd()
dataPath = usr_dir.joinpath("eMolFrag2/unittests/data/db-files")
mol2 = dataPath.joinpath("mol2")
smi = dataPath.joinpath("smi")
sdf = dataPath.joinpath("sdf")
pdb = dataPath.joinpath("pbd")
mol = dataPath.joinpath("mol")

def getOptions(inputPath):

  filePath = usr_dir.joinpath("config.emf")
  f = open("config.emf", "w")
  f.write(f"-i {inputPath} -o /content/out")
  f.close()

  sys.argv = ['/content/eMolFrag2/src/eMolFrag.py',"-c", str(filePath)]
  options = Options.Options()

  return options

def runGetFiles(options, num_expected):
  assert len(MoleculeFileReader.getFiles(options)) == num_expected

def runGetFilesTests():
  testPaths = [mol2, smi, pdb, mol]
  #Tests if mol2 and smi are taken
  for folderPath in testPaths:
      options = getOptions(folderPath)
      runGetFiles(options, 5)
      
  #Will recognize the files as bad
  options = getOptions(sdf)
  runGetFiles(options, 0)

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
    tests = {"getFiles": runGetFilesTests}

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