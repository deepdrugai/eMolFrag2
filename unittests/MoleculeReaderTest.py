import sys
from pathlib import Path
from SuperSecretProject.src.utilities import logging
from SuperSecretProject.src.input import MoleculeReader

usr_dir = Path.cwd()
dataPath = usr_dir.joinpath("SuperSecretProject/unittests/data/db-files")
mol2 = dataPath.joinpath("mol2")
smi = dataPath.joinpath("smi")
sdf = dataPath.joinpath("sdf")
pdb = dataPath.joinpath("pbd")
mol = dataPath.joinpath("mol")

def getListofFiles(folderPath):
  files = []

  for current_file in folderPath.iterdir():
    #if the file extension is not a supportedd format, add the file to the bad file list, otherwise add it to the file list
    files.append(folderPath / current_file.name)

  return files

def runGetMolecules(files, num_expected):
  assert len(MoleculeReader.getMolecules(files)) == num_expected

def runGetMoleculesTests():
  testPaths = [mol2, smi, pdb, mol]
  #Tests if mol2 and smi are taken
  for folderPath in testPaths:
      runGetMolecules(getListofFiles(folderPath), 5)
      
  #Will recognize the files as bad
  runGetMolecules(getListofFiles(sdf), 0)


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
    tests = {"getMolecules": runGetMoleculesTests}

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
            logging.logger.errror(f'Failed {test}.')

if __name__ == "__main__":
    runtests()