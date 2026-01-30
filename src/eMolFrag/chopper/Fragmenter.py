from rdkit import Chem

from eMolFrag.utilities.logging import log


def fragmentToMol(mol: Chem.Mol, frag_as_set, snips) -> Chem.RWMol:
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

    # Set explicit double bonds, remove aromaticity
    Chem.Kekulize(cp, clearAromaticFlags=True)

    # if frag_as_set is not a set (as in freeatom int), convert to set
    if not isinstance(frag_as_set, set):
        frag_as_set = {int(frag_as_set)}
        
    # Counts the number of cuts for each atom in the fragment
    cuts: dict[int, int] = {}
    for a1, a2 in snips:
        a1, a2 = int(a1), int(a2)
        if a1 in frag_as_set and a2 not in frag_as_set:
            cuts[a1] = cuts.get(a1, 0) + 1
        elif a2 in frag_as_set and a1 not in frag_as_set:
            cuts[a2] = cuts.get(a2, 0) + 1

    for atom in sorted(set(range(len(cp.GetAtoms()))) - frag_as_set, reverse=True):
        cp.RemoveAtom(atom)
        
    # Specify radical electrons using the count from cuts
    for atom in cp.GetAtoms():
        if not atom.HasProp("original_idx"):
            continue
        try:
            og = atom.GetIntProp("original_idx")
        except Exception:
            og = int(atom.GetProp("original_idx"))

        n = cuts.get(og, 0)
        if n:
            atom.SetNumRadicalElectrons(n)

    # It is suggested to sanitize fragments
    try:
        Chem.SanitizeMol(cp)
    except Exception as e:
        try:
            log.warning(f"Attempt #2 to sanitize fragment: {frag_as_set}. {e}")
            Chem.SanitizeMol(cp, Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_ADJUSTHS)

        except Exception:
            log.error(f"Fragment {frag_as_set} is not sanitizable.")  
    return cp


def fragmentAll(mol, bricks, linkers, freeatoms, snips):
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
        [fragmentToMol(mol, set(brick), snips) for brick in bricks],
        [fragmentToMol(mol, set(linker), snips) for linker in linkers],
        [fragmentToMol(mol, set(freeatom), snips) for freeatom in freeatoms],
    )
