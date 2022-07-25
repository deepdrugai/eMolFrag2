from rdkit import Chem
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.utilities import logging
from eMolFrag2.src.chopper import BRICS_custom
        
def compute(rdkit_mol, snips):
    """
        Compute all connectivity information for bricks and linkers.
       
        The main algorithm is to identify where dummy atoms would be placed by BRICS
        breaking bonds. Conventiently, given a snip (start, end) where BRICS would
        cleave, one atom in the snip is in a (unique) fragment, while the other atom
        would be a radical (or dummy).

        Connectivity for an atom in a fragment is the atom-type of the dummy

        @input: mol (Rdkit.Mol)
        @input: snips (set of 2-tuples) -- bonds where we would cleave
   """
    # Analyze all snips in both directions
    for (start, end) in list(snips) + [(y, x) for x, y in snips]:

        # Each atom that is part of a BRICS cleave point may have multiple 'radical' connections;
        # use a 'list' to track them all; properties in rdkit are strings
        connections = rdkit_mol.GetAtomWithIdx(start).GetProp(constants.ATOM_CONNECTION_PROP) \
                      if rdkit_mol.GetAtomWithIdx(start).HasProp(constants.ATOM_CONNECTION_PROP) else ''

        # Add the atom type of the 'radical'
        connections += ('' if not connections else ' ') + rdkit_mol.GetAtomWithIdx(end).GetProp(constants.ATOMTYPE_PROP)

        # Get AtomType for end atom and associate it as a conenction for start
        rdkit_mol.GetAtomWithIdx(start).SetProp(constants.ATOM_CONNECTION_PROP, connections)