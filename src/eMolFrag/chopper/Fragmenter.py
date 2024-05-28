from rdkit import Chem

from eMolFrag.utilities.logging import log


def fragmentToMol(mol, frag_as_set):
    """
    Acquire the rdkit molecule corresponding to the fragment specified by the index set (frag_as_set).
    We acquire the fragment (with underlying property information intact) by deletion of all other atoms

    @input: mol (Rdkit.Mol)
    @input: frag (set of int indices) -- indices in the mol corresponding to a fragment

    @output: mol (Rdkit.RWMol) corresponding to the input fragment
    """

    import numpy as np

    # Create copy so we can modify it accordingly
    cp = Chem.RWMol(mol)

    # if frag_as_set contains only one value (as in freeatom), convert to set
    if isinstance(frag_as_set, np.number):
        frag_as_set = set([frag_as_set])

    for atom in sorted(set(range(len(cp.GetAtoms()))) - frag_as_set, reverse=True):
        cp.RemoveAtom(atom)

    # It is suggested to sanitize fragments
    try:
        Chem.SanitizeMol(cp)
        # TODO: Try to figure out the following to sanitize molecules better (not sure if this is necessary)
        # Chem.SanitizeMol(mol, Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_ADJUSTHS)
    except:
        log.warning(f"Fragment {frag_as_set} is not sanitizable.")

    return cp


def fragmentAll(mol, bricks, linkers, freeatoms):
    """
    For each fragment:
       (atom-indices) + mol -> Rdkit.Mol fragment (with connectivity information maintained)

    @input: bricks -- set of tuples of integers
    @input: linkers -- set of tuples of integers

    @output: list of Rdkit.Mols corresponding to bricks
    @output: list of Rdkit.Mols corresponding to linkers
    @output: list of Rdkit.Mols corresponding to freeatoms
    """

    return (
        [fragmentToMol(mol, set(brick)) for brick in bricks],
        [fragmentToMol(mol, set(linker)) for linker in linkers],
        [fragmentToMol(mol, freeatom) for freeatom in freeatoms],
    )
