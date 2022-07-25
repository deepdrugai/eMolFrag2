# Files needed for Deconstructor.py 
from rdkit import Chem
from eMolFrag2.src.utilities import constants, logging
from eMolFrag2.src.chopper import BRICS_custom

# Files needed for testing 
from pathlib import Path
import os
from eMolFrag2.unittests import utilities
from eMolFrag2.src.chopper import Deconstructor 

#
# Call the main method 
#
def run_deconstruct(molPath):
    
    # type of test case - normal 
    # test for equal atom number in original molecule and fragments after deconstruction
    # logging.logger.debug(f'Testing:{molPath.name}')

    # create rdkit molecule from molPath 
    rdkit_mol = utilities.getRDKitMolecule(molPath, Path(molPath).suffix)
    print('create rdkit?', rdkit_mol)
    # remove hydrogen 
    rdkit_mol = Chem.RemoveAllHs(rdkit_mol, sanitize = True)

    # get fragments and sets of chopping points 
    bricks, linkers, snips = Deconstructor.deconstruct(rdkit_mol)
    
    fragments = []

    # count number of atoms in bricks set
    b_count = 0
    for b in bricks: 
      b_count += len(b)
      for t in b: 
        fragments.append(t)

    # count number of atoms in linkers set 
    l_count = 0
    for l in linkers: 
      l_count += len(l)
      for t in l: 
        fragments.append(t)
    
    logging.logger.info(f'# of atoms in the molecule: { len(rdkit_mol.GetAtoms()) }')
    logging.logger.info(f'# of atoms after deconstruct:{ b_count + l_count }')
    
    # Check if there is any overlapped atoms - atoms 
    atoms = []
    for s in snips: 
      atoms += s

    uniqueAtoms = set(atoms)

    diff = 0 
    for atom in uniqueAtoms:
      if not atom in fragments: 
        diff += 1
    
    logging.logger.info(f'Atoms not in bricks or linkers: {diff}')

    # difference = len(atoms) - len(uniqueAtoms)
    logging.logger.info(f'Atoms in Final Snips: {atoms}')
    logging.logger.info(f'Unique atoms in final snips: {uniqueAtoms}')
      
    #
    # Test Normal Case: atoms do not overlap
    #   fragments contain the same number of atoms as the original molecule
    #
    if diff == 0:
      # print("Running Normal Tests")
      assert b_count + l_count == len(rdkit_mol.GetAtoms())

    #
    # Test Overlap Cases: one or more molecule overlap
    #   fragments contain less atoms than the original molecules 
    #
    else:
      # total number of atoms in bricks and linkers 
      #      should equal to number of atoms in original molecule - number of overlapped atoms
      # print("Running Tests with Overlapped Atoms")
      assert b_count + l_count == len(rdkit_mol.GetAtoms()) - diff



def run_deconstructTests():

    cwd = Path.cwd().joinpath("eMolFrag2", "unittests", "data", "uniqueMol(SMI)")

    # Test 1: .smi files with overlapped atoms 
    Overlapped = ['DB00415.smi', 'DB04626.smi', 'DB13499.smi']
    for smi in Overlapped: 
      molPath = cwd.joinpath(smi)
      # run_deconstruct(molPath)


    # Test 2: .smi files with complete number of atoms as the original molecule 
    Normal = ['DB01208.smi', 'DB11774.smi']
    for smi in Normal: 
      molPath = cwd.joinpath(smi)
      # run_deconstruct(molPath)


    # Test 100 antibiotics - mol2 files 
    cwd2 = Path.cwd().joinpath('eMolFrag2', 'test', 'mol2-test')
    antibiotics = []
    directory = '/content/eMolFrag2/test/mol2-test'
    for filename in os.listdir(directory):
      filepath = os.path.join(directory, filename)

      if os.path.isfile(filepath):
        antibiotics.append(filename)
    
    print("Length of file before removing problem files:", len(antibiotics))

    # Run problem files in a separate list 
    problem_files = ['DB01000.mol2', 'DB00948.mol2', 'DB00485.mol2', 
     'DB00301.mol2', 'DB01190.mol2', 'DB01147.mol2', 'DB00713.mol2', 
     'DB01331.mol2', 'DB01061.mol2', 'DB00607.mol2', 'DB00760.mol2', 
     'DB00303.mol2', 'DB00319.mol2']


    kekulize_files = ['DB01328.mol2', 'DB00779.mol2', 'DB01155.mol2',
      'DB00845.mol2', 'DB00430.mol2', 'DB00467.mol2', 'DB01405.mol2',
      'DB01051.mol2', 'DB00537.mol2', 'DB01137.mol2', 'DB00817.mol2',
      'DB00229.mol2', 'DB00487.mol2', 'DB00267.mol2', 'DB01329.mol2',
      'DB00923.mol2', 'DB00218.mol2', 'DB01165.mol2', 'DB01059.mol2',
      'DB01327.mol2', 'DB00274.mol2', 'DB01044.mol2', 'DB01208.mol2',
      'DB00978.mol2', 'DB01326.mol2', 'DB00827.mol2' ]

    # warning - O.co2 with non C.2 or S.o2 neighbor - 5
    antibiotics.remove('DB00355.mol2') 
    antibiotics.remove('DB00698.mol2') 
    antibiotics.remove('DB00911.mol2') 
    antibiotics.remove('DB00446.mol2') 
    antibiotics.remove('DB00916.mol2') 

    print("Length of file after removing problem files:", len(antibiotics))

    for mol in kekulize_files: 
      molPath = cwd2.joinpath(mol)
     
      file_name = molPath.name
      logging.logger.info(f"Testing: {file_name}")
      run_deconstruct(molPath)


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

    #utilities.emit(printlevel, f'Executing {__file__} unit tests.')
    logging.logger.debug(f'Executing {__file__} unit tests.')

    #
    # Define all tests as a Dictionary: {str-name, <function-to-execute>}
    #
    tests = { 
              # "getMolMatrix" : run_getMolMatrixTests, 
              # "molAdjList" : run_molAdjListTests, 
              # "molBRICSBonds" : run_molBRICSBONDSTests, 
              # "molFraments" : run_molFragmentsTests, 
              # "combineAdjLinkerSequences" : run_combineAdjLinkerSequenceTests, 
              # "computeFragmentsAndSnips" : run_computeFragmentsAndSnipsTests, 
              "deconstruct" : run_deconstructTests
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