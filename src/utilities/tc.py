import math 

from rdkit import Chem
from rdkit import DataStructs # For TC Computations
from eMolFrag2.src.utilities import logging
from eMolFrag2.src.representation import Molecule

#
# A utility function to compute the Tanimoto Coefficient
#
def TC_private(rdkit_mol1, rdkit_mol2):

    fp_1 = Chem.RDKFingerprint(rdkit_mol1)
    fp_2 = Chem.RDKFingerprint(rdkit_mol2)

    return DataStructs.FingerprintSimilarity(fp_1, fp_2)

def TC(mol1, mol2):

    if isinstance(mol1, Molecule.Molecule) != isinstance(mol2, Molecule.Molecule):
        logging.logger.error(f'Molecule objects of different type in TC computation')
        return -1

    return (TC_private(mol1.getRDKitObject(), mol2.getRDKitObject()) \
            if isinstance(mol1, Molecule.Molecule) else TC_private(mol1, mol2))
            

def TCEquiv(mol1, mol2, tc_threshold = 1.0):
    """
        @input: 2 Molecule objects
        @output: True if the molecules are TC-equivalent; False otherwise
                (we use math.isclose to assess floating-point-based equivalent)   
    """
    tanimoto = TC(mol1, mol2)  

    # >   
    if (tanimoto > tc_threshold):
        return True
  
    # =                                         # 4-decimal place equality 
    return math.isclose(tanimoto, tc_threshold, rel_tol = 1e-5)