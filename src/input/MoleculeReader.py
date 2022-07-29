from pathlib import Path

from rdkit import Chem
# from rdkit import RDLogger

from eMolFrag2.src.representation.Molecule import Molecule
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.utilities.logging import log


def fileToString(file):
    """
        Read the entire contents of a file into a string

        @input: file -- valid path to a file
    """
    contents = ""
    with open(file) as f:
        contents = f.read()

    return contents


def to_mol(molPath):
    """ Create Molecule object from file path (string) """
    mol = getRDKitMolecule(molPath)
    m = Molecule(mol, molPath.name)
    return m


def getRDKitMolecule(path, extension=None):
    """
        Given a path object, return the corresponding RDKit molecule object
        This simplified functionality is for testing only
    """
    content = fileToString(path)
    path = path if isinstance(path, Path) else Path(path)
    return convertToRDkit(content, path)


def convertToRDkit(contents, path):
    """
        Attempt to read and convert the input file into an RdKit.Mol object

        @input: contents -- string contents of a file
        @input: mol)file -- input molecule file name

        @output: tuples: id, rdkit_mol
    """
    #Chem.doKekule = False
    extension = path.suffix
    # log.debug(f"Running {path}, with extension: {extension}.")

    if extension not in constants.ACCEPTED_FORMATS:
        log.error(f'Input file type with extension {extension} ({path.name}) not supported.')
        return None

    elif (extension == constants.MOL2_FORMAT_EXT):
        mol = readMol2File(contents)
        if mol is None:
            print()
            log.error(f"Rdkit failed to process file {path.name}.")
            return None
        return mol

    elif (extension == constants.SMILES_FORMAT_EXT):
        return Chem.MolFromSmiles(contents)

        # TODO Fix SmilesReader
        # from eMolFrag2.src.input import SmilesReader
        # return SmilesReader.readSmilesFile(contents)

    #
    # Other file formats that do not support AtomTypes
    #
    elif (extension == constants.FASTA_FORMAT_EXT):
        mol = Chem.MolFromFASTA(contents)

    elif (extension == constants.YAML_FORMAT_EXT):
        mol = Chem.MolFromHELM(contents)

    elif (extension == constants.MOL_FORMAT_EXT):
        mol = Chem.MolFromMolBlock(contents)

    elif (extension == constants.PDB_FORMAT_EXT):
        mol = Chem.MolFromPDBBlock(contents)

    elif (extension == constants.SMARTS_FORMAT_EXT):
        mol = Chem.MolFromSmarts(contents)

    elif (extension == constants.TPL_FORMAT_EXT):
        mol = Chem.MolFromTPLBlock(contents)

    if not mol:
        log.error(f'Molecule file ({path.name}) was not read in due to RDKit Error.')
        return None

    if path:
        log.warning(f'Input file type {extension} ({path.name}) will not preserve molecule SYBL atom types.')
        return mol


def readMol2File(contents):
    # Turn off rdkit error messages
    # RDLogger.DisableLog('rdApp.*')

    try:
        return Chem.MolFromMol2Block(contents)
    except Exception:
        pass
    try:
        return Chem.MolFromMol2Block(contents, kekulize=False)
    except Exception:
        pass
    try:
        return Chem.MolFromMol2Block(contents, kekulize=False, sanitize=False)
    except Exception:
        pass
    try:
        return Chem.MolFromMol2Block(contents, sanitize=False)
    except Exception:
        pass
    try:
        return Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False)
    except Exception:
        pass
    try:
        return Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False, cleanupSubstructures=False)
    except Exception:
        pass


def getMolecules(files):
    """
        From the set of input files, acquire the corresponding Rdkit molecules.

        @input: The list of input files
        @output: Molecule objects (each containing an Rdkit.Mol object)

        USER ISSUE: WHAT if a file with multiple molecules is input?
    """
    mols = []

    for current_file in files:

        # get the contents of the file and the file type (extension) for processing
        file_contents = fileToString(current_file)

        # Attempt to interpret the molecule
        try:
            mol = convertToRDkit(file_contents, current_file)
        except:
            log.error(f'RDKit failed to read {current_file.name}', exc_info=True)
            break

        # add it to our dataset and update the filenames we have
        if mol is not None:
            mols.append(Molecule(mol, current_file.name))

    if mols is None:
        log.error(f"No molecules generated from files list: {[x.name for x in files]}.")

    return mols
