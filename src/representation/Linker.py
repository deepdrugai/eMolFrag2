from rdkit import Chem

from SuperSecretProject.src.representation import Molecule
from SuperSecretProject.src.utilities import constants

class Linker(Molecule.Molecule):

    def __init__(self, rdkit_mol, parent, suffix = 0):
        """
            @input: rdkit_obj -- Rdkit.Mol object representing this fragment
            @input: num_suf -- numeric suffix to differentiate the fragment from other fragments
            @input: parent -- Molecule object (contains origin information for this fragment) 
        """
        Molecule.Molecule.__init__(self, rdkit_mol, parentMol = parent)

        self.filename = self.makeFragmentFileName(parent.getFileName(), \
                                                  prefix = constants.LINKER_PREFIX, \
                                                  numeric_suffix = suffix)
        
    def toSDF(self):
        """
            Assuming a molecule with AtomType and connectivity
            information preseversed, output the molecule in SDF format
            with proper appendices

            @output: string in SDF format
        """
        self.clearProperties()

        # A linker maintains a "maximum number of connections for each fragment"
        # All atoms must have an atomtype; not all atoms have connections
        appendix = '\n'.join(f'{str(len(atom.GetProp(constants.ATOM_CONNECTION_PROP).split()) if atom.HasProp(constants.ATOM_CONNECTION_PROP) else 0)} {atom.GetProp(constants.ATOMTYPE_PROP)}'\
                             for atom in self.rdkitObject.GetAtoms())

        self.rdkitObject.SetProp(constants.SDF_OUTPUT_LINKER_CONNECTIONS, appendix)

        return self._toSDF()
    