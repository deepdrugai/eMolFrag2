from pathlib import Path

import sys
from eMolFrag2.unittests import utilities
from eMolFrag2.src.representation import Molecule, MoleculeDatabase
from eMolFrag2.src.utilities import tc    # _TCEquiv tests


def run_add(md, molPath, expec_result):

    # Create rdkit object from file path           extension
    mol = utilities.getRDKitMolecule(molPath, Path(molPath).suffix)
    Mol = Molecule.Molecule(mol, molPath.name)
    assert md.add(Mol) == expec_result 

def run_addTests():

    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")
    md = MoleculeDatabase.MoleculeDatabase(given_tc = 1.0)

    # Molecules with tc = 1.0
    mol1 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol2 = cwd.joinpath("similarPairSMI/3/DB16219.smi")

    run_add(md, mol1, True)
    run_add(md, mol1, False)
    run_add(md, mol2, False)

    # Molecules with tc < 1.0
    uniqueMol1 = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    uniqueMol2 = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    uniqueMol3 = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")
    uniqueMol4 = cwd.joinpath("uniqueMol(SMI)/DB11774.smi")
    uniqueMol5 = cwd.joinpath("uniqueMol(SMI)/DB13499.smi")

    run_add(md, uniqueMol1, True)
    run_add(md, uniqueMol2, True)
    run_add(md, uniqueMol3, True)
    run_add(md, uniqueMol4, True)
    run_add(md, uniqueMol5, True)
    

# return the list of UNIQUE database
def run_addAll(md, moleculesPath, length):
    molecules = []

    for molPath in moleculesPath: 
      # 1. create rdkit object 
      mol = utilities.getRDKitMolecule(molPath, Path(molPath).suffix)
      # 2. create a local molecule, take in (rdkit_object and file_name )
      Mol = Molecule.Molecule(mol, molPath.name)
      # 3. add local molecule to a list 
      molecules.append(Mol)

    # frequency = md.addAll(molecules)
    # print("Size of list:\n", len(frequency))
    # print(frequency)

    # Test the size of the list 
    assert len(md.addAll(molecules)) == length

def run_addAllTests():
    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")
    md1 = MoleculeDatabase.MoleculeDatabase(given_tc = 1.0)
    moleculesPath = []

    # Test 1: adding 5 unique molecules 
    uniqueMol1 = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    uniqueMol2 = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    uniqueMol3 = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")
    uniqueMol4 = cwd.joinpath("uniqueMol(SMI)/DB11774.smi")
    uniqueMol5 = cwd.joinpath("uniqueMol(SMI)/DB13499.smi")
    
    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_addAll(md1, moleculesPath, 5)

    # Test 2: add pairs of similar molecules (tc = 1.0)
    mol1 = cwd.joinpath("similarPairSMI/1/DB00452.smi")
    mol2 = cwd.joinpath("similarPairSMI/1/DB01421.smi")
    moleculesPath.clear()
    moleculesPath.extend([mol1, mol2])
    run_addAll(md1, moleculesPath, 1)

    # Test 3: add 2nd pair of similar molecules
    mol3 = cwd.joinpath("similarPairSMI/2/DB01137.smi")
    mol4 = cwd.joinpath("similarPairSMI/2/DB01165.smi")
    moleculesPath.extend([mol3, mol4])
    run_addAll(md1, moleculesPath, 1)

    # Test 4: add 3 sets of 2 similar molecules 
    md2 = MoleculeDatabase.MoleculeDatabase()
    mol5 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol6 = cwd.joinpath("similarPairSMI/3/DB16219.smi")
    moleculesPath.extend([mol5, mol6])
    run_addAll(md2, moleculesPath, 3)

    # Test 5: create a new database and add all 11 molecules at once 
    md3 = MoleculeDatabase.MoleculeDatabase()
    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_addAll(md3, moleculesPath, 8)


def run_GetUniqueMolecules(moleculesPath, size):
    database = MoleculeDatabase.MoleculeDatabase(given_tc = 1.0)
    molecules = []
    for molPath in moleculesPath: 
      # 1. create rdkit object, take in (file_path, file_extension)
      mol = utilities.getRDKitMolecule(molPath, Path(molPath).suffix)
      # 2. create a local molecule, take in (rdkit_object and file_name)
      Mol = Molecule.Molecule(mol, molPath.name)
      # 3. add local molecule to a list 
      molecules.append(Mol)

    database.addAll(molecules)
  
    assert len(database.GetUniqueMolecules()) == size

def run_GetUniqueMoleculesTests():

    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")
    moleculesPath = []

    # Test 1: adding 5 unique molecules 
    uniqueMol1 = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    uniqueMol2 = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    uniqueMol3 = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")
    uniqueMol4 = cwd.joinpath("uniqueMol(SMI)/DB11774.smi")
    uniqueMol5 = cwd.joinpath("uniqueMol(SMI)/DB13499.smi")

    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_GetUniqueMolecules(moleculesPath, 5)

    # Test 2: adding 3 sets of 2 similar molecules 
    mol1 = cwd.joinpath("similarPairSMI/1/DB00452.smi")
    mol2 = cwd.joinpath("similarPairSMI/1/DB01421.smi")
    mol3 = cwd.joinpath("similarPairSMI/2/DB01137.smi")
    mol4 = cwd.joinpath("similarPairSMI/2/DB01165.smi")
    mol5 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol6 = cwd.joinpath("similarPairSMI/3/DB16219.smi")

    moleculesPath.clear()
    moleculesPath.extend([mol1, mol2, mol3, mol4, mol5, mol6])
    run_GetUniqueMolecules(moleculesPath, 3)

    # Test 3: add 11 molecules at once 
    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_GetUniqueMolecules(moleculesPath, 8)



def run_GetAllMolecules(moleculesPath, size):
    
    database = MoleculeDatabase.MoleculeDatabase(given_tc = 1.0)
    molecules = []
    
    # convert each file path to local molecule and add to a list 
    for molPath in moleculesPath: 
      # 1. create rdkit object 
      mol = utilities.getRDKitMolecule(molPath, Path(molPath).suffix)
      # 2. create a local molecule, take in (rdkit_object and file_name )
      Mol = Molecule.Molecule(mol, molPath.name)
      # 3. add local molecule to a list 
      molecules.append(Mol)

    database.addAll(molecules)
    
    assert len(database.GetAllMolecules()) == size

  

def run_GetAllMoleculesTests():
    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data")
    moleculesPath = []

    # Test 1: adding 5 unique molecules 
    uniqueMol1 = cwd.joinpath("uniqueMol(SMI)/DB00415.smi")
    uniqueMol2 = cwd.joinpath("uniqueMol(SMI)/DB01208.smi")
    uniqueMol3 = cwd.joinpath("uniqueMol(SMI)/DB04626.smi")
    uniqueMol4 = cwd.joinpath("uniqueMol(SMI)/DB11774.smi")
    uniqueMol5 = cwd.joinpath("uniqueMol(SMI)/DB13499.smi")

    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_GetAllMolecules(moleculesPath, 5)

    # Test 2: adding 3 sets of 2 similar molecules 
    mol1 = cwd.joinpath("similarPairSMI/1/DB00452.smi")
    mol2 = cwd.joinpath("similarPairSMI/1/DB01421.smi")
    mol3 = cwd.joinpath("similarPairSMI/2/DB01137.smi")
    mol4 = cwd.joinpath("similarPairSMI/2/DB01165.smi")
    mol5 = cwd.joinpath("similarPairSMI/3/DB12447.smi")
    mol6 = cwd.joinpath("similarPairSMI/3/DB16219.smi")

    moleculesPath.clear()
    moleculesPath.extend([mol1, mol2, mol3, mol4, mol5, mol6])
    run_GetAllMolecules(moleculesPath, 6)

    # Test 3: adding 11 molecules at once 
    moleculesPath.extend([uniqueMol1, uniqueMol2, uniqueMol3, uniqueMol4, uniqueMol5])
    run_GetAllMolecules(moleculesPath, 11)


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
    tests = { # "_TCEquiv" : run_TCEquivTests,
              "add" : run_addTests,
              "addAll" : run_addAllTests,
              "GetUniqueMolecules" : run_GetUniqueMoleculesTests,
              "GetAllMolecules" : run_GetAllMoleculesTests,
              "numUnique" : run_numUniqueTests, 
              "numAllMolecules" : run_numAllMolecules 
            }
    #
    # Run 
    #
    successful = []
    failed = []

    for(test_name, test_func) in tests.items():
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
