from pathlib import Path

from SuperSecretProject.src.representation import Molecule
from SuperSecretProject.src.utilities import constants
from SuperSecretProject.src.utilities import logging

#
# We will handle two formats for SMILES; these formats can be intermixed
# in the same file:
#    (1) a file containing a sequence of SMILES-formatted molecules
#          * In this case, the names of the molecules will be the SMILES-text
#
#    (2) a file with a sequence of pairs of (id, smiles) in the form:
#          SMILES-1 id-1
#          SMILES-2 id-2
#          ...
#          SMILES-n id-n
#
def parse(contents):
    """
        @input: contents -- the file contents as a string
        @output: a list of tuples of the form [(id, SMILES)]
    """
    mols = []

    for line in contents.split('\n'):

        # Tokenize while trimming whitespace
        tokens = [token.strip() for token in line.split()]

        # A molecule is its own ID
        if len(tokens) == 1:
            mols.append((tokens[0], tokens[0]))

        # An ID has been specified
        elif len(tokens) == 2:
            mols.append((tokens[1], tokens[0]))
        
        elif len(tokens) > 2:
            logging.logger.error(f'Expected SMILES file format. Either MOL\n or "smi id" expected, not {line}')        

        else:
            pass # Ignore blank lines

    return mols

def toRdkitMol(mol_id, mol_smi_str):
    """
        In order to compute and preserve AtomTypes, we use
        OpenBabel's conversion code to acquire and write those types.

        @input: contents -- the file contents as a string
        @output: list of Molecule objects
    """
    from rdkit import Chem
    rdkit_mol = Chem.MolFromSmiles(mol_smi_str)

    try:
        import pybel
    except:
        logging.logger.error(f'OpenBabel has not been installed; atom types of input SMILES molecules will not be preserved.')
        return mol_id, rdkit_mol

    # Convert SMI -> Mol2 to acquire AtomTypes
    obabel_mol = pybel.readstring('smi', mol_smi_str)

    # Associate the OpenBabel atom types with our Rdkit molecule    
    for index, obabel_atom in enumerate(obabel_mol.atoms):
        # BREAKING here: rdkit_mol.GetAtomWithIdx(index - 1).SetProp(constants.ATOMTYPE_PROP, obabel_atom.type)
     
    return mol_id, rdkit_mol

def readSmilesFile(contents):
    """
        In order to compute and preserve AtomTypes, we use
        OpenBabel's conversion code to acquire and write those types.

        @input: contents -- the file contents as a string
        @output: list of Molecule objects
    """
    return [toRdkitMol(mol_id, mol_str) for mol_id, mol_str in parse(contents)]