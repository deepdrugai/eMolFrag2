from rdkit import Chem
from eMolFrag.utilities.logging import log
from eMolFrag.utilities import constants

# from eMolFrag.chopper import Deconstructor
# from eMolFrag.chopper import Connectivity


def ensureAtomTypeIntegrity(mol):
    """
    If the atom type for each atom is not specified, substitute the atom symbol.

    @output: True if all AtomTypes are defined
             False if any AtomTypes have been substituted
    """
    hasIntegrity = True

    for atom in mol.GetAtoms():
        if not atom.HasProp(constants.ATOMTYPE_PROP):
            hasIntegrity = False
            atom.SetProp(constants.ATOMTYPE_PROP, atom.GetSymbol())

    return hasIntegrity


def preprocess(rdkit_mol):
    """
    Before chopping, we want to ensure that:
        (0) Our computations will be based on a COPY of the original molecule
        (1) all hydrogens are removed
        (2) Some form of Atom Type information is maintained in the molecule

    @input: Rdkit.Mol
    @output: Rdkit.Mol -- Copy of the input molecule prepared for fragmentation
    """
    # (0) Make a Read / Write version of the molecule
    cp_mol = Chem.RWMol(rdkit_mol)

    # (1) Remove all hydrogens from our molecule
    try:
        cp_mol = Chem.RemoveAllHs(cp_mol)
    except Exception:
        log.error(f"Fragment {cp_mol} hydrogens can not be removed.")

    #
    # (2) Ensure we have atomtype information for all atoms
    #
    if not ensureAtomTypeIntegrity(cp_mol):
        log.warning(f"molecule does not have Tripos AtomTypes specified or computed; using Atom symbols as substitute")

    return cp_mol
