from rdkit import Chem

from eMolFrag2.src.representation import Molecule
from eMolFrag2.src.utilities import constants

class Brick(Molecule.Molecule):

    def __init__(self, rdkit_mol, parent, suffix = 0):
        """
            @input: rdkit_obj -- Rdkit.Mol object representing this fragment
            @input: num_suf -- numeric suffix to differentiate the fragment from other fragments
            @input: parent -- Molecule object (contains origin information for this fragment) 
        """
        Molecule.Molecule.__init__(self, rdkit_mol, parentMol = parent)

        self.filename = self.makeFragmentFileName(parent.getFileName(), \
                                                  prefix = constants.BRICK_PREFIX, \
                                                  numeric_suffix = suffix)
        
    def toSDF(self):
        """
            Assuming a molecule with AtomType and connectivity
            information preseversed, output the molecule in SDF format
            with proper appendices

            @output: string in SDF format
        """
        self.clearProperties()

        # ATOMTYPES appendix; take directly from Atom.Prop information
        self.rdkitObject.SetProp(constants.SDF_OUTPUT_BRICK_ATOMTYPES, '\n'.join([atom.GetProp(constants.ATOMTYPE_PROP) for atom in self.rdkitObject.GetAtoms()]))

        # Break connection string in separate cases...and join all together
        # Multiple connections may be stored as a comma-separated string for an atom
        # e.g., (1, C.3 C.3 N.4) -->
        #                2 C.3
        #                2 C.3
        #                2 N.4        
        atom_conn_map = {index : atom.GetProp(constants.ATOM_CONNECTION_PROP) for index, atom in enumerate(self.rdkitObject.GetAtoms()) if atom.HasProp(constants.ATOM_CONNECTION_PROP)}
        
        appendix = ''.join(''.join(f'{atom_index + 1} {atomtype}\n' for atomtype in atom_conn_map[atom_index].split(' ')) for atom_index in atom_conn_map)
        
        self.rdkitObject.SetProp(constants.SDF_OUTPUT_BRICK_CONNECTIONS, appendix)

        return self._toSDF()