from pathlib import Path

import utilities
from SuperSecretProject.src.chopper import Chopper


def runisBrick(filepath, expec_result):

    mol = utilities.getRDKitMolecule(Path(filepath))
    assert Chopper.isBrick(mol) == expec_result

def runIsBrickTests():
    
    runisBrick("./data/1098067-c2-c2-double-bond/b-CHEMBL1098067.mol2-000.sdf", True)
    runisBrick("./data/1098067-c2-c2-double-bond/b-CHEMBL1098067.mol2-001.sdf", True)        
    runisBrick("./data/1098067-c2-c2-double-bond/b-CHEMBL1098067.mol2-002.sdf", True)
    
    runisBrick("./data/1098067-c2-c2-double-bond/1-CHEMBL1098067.mol2-000.sdf", False)
    runisBrick("./data/1098067-c2-c2-double-bond/1-CHEMBL1098067.mol2-001.sdf", False)
    runisBrick("./data/1098067-c2-c2-double-bond/1-CHEMBL1098067.mol2-002.sdf", False)

#
#
# Unit test initiation functionality
#
#
def run(func):

    try:
       func()
       return True

    except:
       return False

def runtest(test_name, test_func, successful, failed):
    (successful if run(test_func) else failed).append(test_name)
    
def runtests(printlevel):

    utilities.emit(printlevel, f'Executing {__file__} unit tests.')

    #
    # Define all tests as a Dictionary: {str-name, <function-to-execute>}
    #
    tests = { "isBrick" : runIsBrickTests \
            }

    #
    # Run
    #
    successful = []
    failed = []
    for (test_name, test_func) in tests.items():
        runtest(test_name, test_func, successful, failed)

    # 
    # Report
    #
    if not failed:        
        utilities.emit(printlevel, f'{__name__} unit tests are successful.')

    else:
        for test in failed:
            utilities.emit(printlevel+1, f'Failed {test}.')

if __name__ == "__main__":
    runtests(0)