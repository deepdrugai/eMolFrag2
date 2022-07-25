from pathlib import Path 

import sys 
from eMolFrag2.src.utilities import tc, logging, constants
from eMolFrag2.src.representation import Molecule 
from eMolFrag2.unittests import utilities

#
# Test tanimoto coefficient calculation from two rdkit molecules 
#
def run_TC_private(mol1path, mol2path, expec_result):
    
    rdkit_mol1 = utilities.getRDKitMolecule(mol1path, Path(mol1path).suffix)
    rdkit_mol2 = utilities.getRDKitMolecule(mol2path, Path(mol2path).suffix)
   
    tanimoto = tc.TC_private(rdkit_mol1, rdkit_mol2)
    # Show tc value for testing molecules 
    logging.logger.info(f'TC value for {mol1path.name} and {mol2path.name} is: {tanimoto}' )

    assert tanimoto == expec_result

def run_TC_privateTests():

    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")

    # Test 1: a pair of molecules (.smi) with tc = 1.0 
    # set 1
    mol1 = cwd.joinpath("similarPairSMI/1/DB00452.smi")
    mol2 = cwd.joinpath("similarPairSMI/1/DB01421.smi") 
    run_TC_private(mol1, mol2, 1.0) 

    # set 2 
    mol3 = cwd.joinpath("similarPairSMI/2/DB01137.smi")
    mol4 = cwd.joinpath("similarPairSMI/2/DB01165.smi")
    run_TC_private(mol3, mol4, 1.0) 

    # set 3 
    mol5 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol6 = cwd.joinpath("similarPairSMI/3/DB16219.smi")
    run_TC_private(mol5, mol6, 1.0)   



#
# Checks if two molecules match types and calculat tc value 
#
def run_TC(mol1, mol2, expec_result):
    
    result = tc.TC(mol1, mol2)
                                    # 3 decimal places accuracy 
    assert abs(result - expec_result) <= 0.001


def run_TCTests():
    
    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")

    mol1path = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    mol2path = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    mol3path = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")

    # Create rdkit molecules and local Molecules 
    mol1 = utilities.getRDKitMolecule(mol1path,Path(mol1path).suffix)
    Mol1 = Molecule.Molecule(mol1, mol1path.name)

    mol2 = utilities.getRDKitMolecule(mol2path,Path(mol2path).suffix)
    Mol2 = Molecule.Molecule(mol2, mol2path.name)

    mol3 = utilities.getRDKitMolecule(mol3path,Path(mol3path).suffix)
    Mol3 = Molecule.Molecule(mol3, mol3path.name)

    # Test 1: different molecule type (1 rdkit_mol, 1 local molecule)
    run_TC(mol1, Mol2, -1)
    run_TC(Mol1, mol2, -1)

    # Test 2: two rdkit_mol 
    run_TC(mol1, mol2, 0.444) 
    run_TC(mol1, mol3, 0.293)
    run_TC(mol2, mol3, 0.311)

    # Test 3: two local molecules 
    run_TC(Mol1, Mol2, 0.444) 
    run_TC(Mol1, Mol3, 0.293)
    run_TC(Mol2, Mol3, 0.311)


def run_TCEquiv(mol1path, mol2path, expec_result):

    mol1 = utilities.getRDKitMolecule(mol1path,Path(mol1path).suffix)
    Mol1 = Molecule.Molecule(mol1, mol1path.name)

    mol2 = utilities.getRDKitMolecule(mol2path,Path(mol2path).suffix)
    Mol2 = Molecule.Molecule(mol2, mol2path.name)

    assert tc.TCEquiv(Mol1.getRDKitObject(), Mol2.getRDKitObject()) == expec_result

def run_TCEquivTests():

    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")

    # Test tc unique molecules (antibiotics with tc < 1.0 )
    mol1path = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    mol2path = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    mol3path = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")

    run_TCEquiv(mol1path, mol2path, False)
    run_TCEquiv(mol1path, mol3path, False)
    run_TCEquiv(mol2path, mol3path, False)


    # Test similar pair antibiotics 
    # set 1
    mol1 = cwd.joinpath("similarPairSMI/1/DB00452.smi")
    mol2 = cwd.joinpath("similarPairSMI/1/DB01421.smi") 
    run_TCEquiv(mol1, mol2, True) 

    # set 2 
    mol3 = cwd.joinpath("similarPairSMI/2/DB01137.smi")
    mol4 = cwd.joinpath("similarPairSMI/2/DB01165.smi")
    run_TCEquiv(mol3, mol4, True)
    
    # prove sets of pairs of molecules do not have tc_equiv
    run_TCEquiv(mol1, mol3, False) 
    run_TCEquiv(mol1, mol4, False) 
    run_TCEquiv(mol2, mol3, False) 
    run_TCEquiv(mol2, mol4, False) 

    # set 3 
    mol5 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol6 = cwd.joinpath("similarPairSMI/3/DB16219.smi")
    run_TCEquiv(mol5, mol6, True)     

    # Test tc unique molecules (tc < 1.0)
    uniqueMol1 = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    uniqueMol2 = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    uniqueMol3 = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")
    uniqueMol4 = cwd.joinpath("uniqueMol(SMI)/DB11774.smi")
    uniqueMol5 = cwd.joinpath("uniqueMol(SMI)/DB13499.smi")

    run_TCEquiv(uniqueMol1, uniqueMol2, False)
    run_TCEquiv(uniqueMol1, uniqueMol3, False)
    run_TCEquiv(uniqueMol1, uniqueMol4, False)
    run_TCEquiv(uniqueMol1, uniqueMol5, False)

    run_TCEquiv(uniqueMol2, uniqueMol3, False)
    run_TCEquiv(uniqueMol2, uniqueMol4, False) 
    run_TCEquiv(uniqueMol2, uniqueMol5, False)

    run_TCEquiv(uniqueMol3, uniqueMol4, False)
    run_TCEquiv(uniqueMol3, uniqueMol5, False)
    
    run_TCEquiv(uniqueMol4, uniqueMol5, False)



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
    tests = { 
              "TC_private" : run_TC_privateTests,
              "TC" : run_TCTests,
              "TCEquiv" : run_TCEquivTests
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