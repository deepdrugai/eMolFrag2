from rdkit import Chem
from eMolFrag2.src.utilities import logging

def fragmentToMol(mol, frag_as_set):
    """
        Acquire the rdkit molecule corresponding to the fragment specified by the index set (frag_as_set).
        We acquire the fragment (with underlying property information intact) by deletion of all other atoms

        @input: mol (Rdkit.Mol)
        @input: frag (set of int indices) -- indices in the mol corresponding to a fragment

        @output: mol (Rdkit.RWMol) corresponding to the input fragment
    """
    # Create copy so we can modify it accordingly
    cp = Chem.RWMol(mol)

    for atom in sorted(set(range(len(cp.GetAtoms()))) - frag_as_set, reverse = True):
        cp.RemoveAtom(atom)
    
    # It is suggested to sanitize fragments
    try:
        Chem.SanitizeMol(cp)
    except:
        logging.logger.warning(f'Fragment {frag_as_set} is not sanitizable.')
    
    return cp

def fragmentAll(mol, bricks, linkers):
    """
         For each fragment:
            (atom-indices) + mol -> Rdkit.Mol fragment (with connectivity information maintained)
            
         @input: bricks -- set of tuples of integers
         @input: linkers -- set of tuples of integers
         
         @output: list of Rdkit.Mols corresponding to bricks
         @output: list of Rdkit.Mols corresponding to linkers
    """
    return [fragmentToMol(mol, set(brick)) for brick in bricks], \
           [fragmentToMol(mol, set(linker)) for linker in linkers]