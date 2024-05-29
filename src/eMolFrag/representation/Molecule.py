#
# The molecule class will contain the rdkit object, the name of the file it came from, as well as a list of 'equal other fragments'.
#

from eMolFrag.utilities import constants, tc
from eMolFrag.utilities.logging import log


class Molecule:
    def __init__(self, rdkit_mol, file_name=None, parentMol=None):
        """
        @input: Rdkit.Mol object for this molecule
        @input: file_name -- file which this molecule originated
                   * In the case where our molecule is a fragment
                     (Brick / Linker) this will be None
        @input: parent -- Molecule that was fragmented to acquire this object
                   * In the case where our molecule is direct from a file,
                     this will be None
        """
        self.rdkitObject = rdkit_mol
        self.filename = file_name
        self.parent = parentMol
        self.similar = []

        # Assign original molecule idx to every atom if mol not a fragment
        if parentMol is None and rdkit_mol:
            for a in rdkit_mol.GetAtoms():
                a.SetIntProp("original_idx", a.GetIdx())

    def fragment(self):
        return bool(self.parent)

    def getParent(self):
        return self.parent

    def getRDKitObject(self):
        return self.rdkitObject

    def getFileName(self):
        return self.filename

    def addTCSimilar(self, mol):
        """
        @input: mol -- a Molecule object that is checked for TC equivalence externally
        """
        return self.similar.append(mol)

    def clearProperties(self):
        """
        Clean the rdkit molecule of all 'public' properties and 'private'
        Tripos ChargeType information

         @input: Rdkit.Mol
         @output: None
        """
        properties = self.rdkitObject.GetPropNames()
        properties.append(constants.ATOMTYPE_PROP)  # Remove an errant property
        properties.append(constants.ATOMTYPE_CHARGE_PROP)  # Remove an errant property
        for prop in properties:
            self.rdkitObject.ClearProp(prop)

    def __hash__(self):
        # hash(custom_object)
        return self.rdkitObject.__hash__()

    def __eq__(self, molecule):
        return tc.TCEquiv(self, molecule)

    def __str__(self):
        numAtoms = self.rdkitObject.GetNumAtoms()
        numBonds = self.rdkitObject.GetNumAtoms()

        return f"{self.filename} has {numAtoms} atoms and {numBonds} bonds"

    def makeFragmentFileName(self, file_name, prefix="", numeric_suffix=0, extension=constants.SDF_FORMAT_EXT):
        return f"{prefix}-{file_name}-{str(numeric_suffix).zfill(3)}{extension}"

    def _toSDF(self):
        """
        Constructs common SDF format information among Brick and Linker fragments

        Common Brick and Linker properties include:
           (1) Name of the Fragment
           (2) A list of TC-equivalent fragments

        @output: SDF format as string
        """

        #
        # Name this molcule: First line in SDF output
        #
        self.rdkitObject.SetProp("_Name", self.getFileName())  # set a title line

        #
        # Appendix consisting of all similar fragments (from the Database equivalence class)
        #
        similar_appendix = "\n".join(sim_mol.getFileName() for sim_mol in self.similar)
        self.rdkitObject.SetProp(constants.SDF_OUTPUT_SIMILAR_FRAGMENTS, similar_appendix)

        def get_sdf_string(molecule):
            # Adjust properties and handle aromaticity without forcing kekulization
            molecule.UpdatePropertyCache(strict=False)
            Chem.GetSymmSSSR(molecule)
            Chem.SanitizeMol(molecule, Chem.SANITIZE_ALL ^ Chem.SANITIZE_KEKULIZE)
            return Chem.MolToMolBlock(molecule)
            # writer.write(molecule)

        from rdkit import Chem

        def try_kekulize(mol):
            Chem.Kekulize(mol, clearAromaticFlags=True)
            return Chem.MolToMolBlock(mol)

        #
        # Output the SDF formated string
        #
        from rdkit.six import StringIO

        sio = StringIO()
        writer = Chem.SDWriter(sio)
        sdf_string = ""

        try:
            log.debug(f"Writing {self.filename} to sdf.")
            writer.write(self.rdkitObject)
        except Chem.rdchem.KekulizeException:
            log.warning(f"SDWriter failed to write {self.filename} to sdf. Trying with molecule.UpdatePropertyCache(strict=False).")
            try:
                log.warning(f"Writing {self.filename} to file with molecule.UpdatePropertyCache(strict=False).")
                self.rdkitObject.UpdatePropertyCache(strict=False)
                writer.write(self.rdkitObject)
            except Chem.rdchem.KekulizeException:
                log.warning(f"SDWriter failed to write {self.filename} to sdf. Trying get_sdf_string.")
                sdf_string = get_sdf_string(self.rdkitObject)
                if sdf_string:
                    log.error(f"{self.filename} SDF string generation successful without kekulization (No Properties).")
                else:
                    log.error(f"Failed at get_sdf_string({self.filename}).")
                    # sdf_string = try_kekulize(self.rdkitObject)
                    # if sdf_string:
                    #     log.warning(f"{self.filename} SDF generation successful with manual kekulization.")
                    # else:
                    #     log.error(f"Manual kekulization of {self.filename} failed.")
        except Exception as e:
            log.error(f"Failed to write mol to file: {e!s}")
        finally:
            writer.close()

        return sdf_string or sio.getvalue()
        # suppl = Chem.ResonanceMolSupplier(self.rdkitObject, Chem.KEKULE_ALL)
        # mols = [self.rdkitObject] + [m for m in suppl]
        # log.info(mols)
        # smilewriter = Chem.SmilesWriter("self.rdkitObject")
        # smilewriter.write(sio)
