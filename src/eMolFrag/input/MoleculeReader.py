from pathlib import Path

from rdkit import Chem

from eMolFrag.output.Mol2Writer import _sybyl_atom_type
from eMolFrag.representation.Molecule import Molecule
from eMolFrag.utilities import constants
from eMolFrag.utilities.logging import log


def fileToString(file):
    """
    Read the entire contents of a file into a string

    @input: file -- valid path to a file
    """
    with open(file) as f:
        return f.read()


def to_mol(molPath):
    """Create Molecule object from file path (string)"""
    mol = getRDKitMolecule(molPath)
    return Molecule(mol, molPath.name)


def getRDKitMolecule(path):
    """
    Given a path object, return the corresponding RDKit molecule object
    WARNING: If file contains multiple molecules getRDKitMolecule only returns first mol.
    """
    content = fileToString(path)
    path = path if isinstance(path, Path) else Path(path)
    mol = convertToRDkit(content, path)
    return mol[0][1] if isinstance(mol, list) else mol


def convertToRDkit(contents, path):
    """
    Attempt to read and convert the input file into an RdKit.Mol object

    @input: contents -- string contents of a file
    @input: mol_file -- input molecule file name

    @output: rdkit_mol -- rdkit molecule object
    """

    extension = path.suffix
    log.debug(f"Running {path} as extension: {extension}.")

    if extension not in constants.ACCEPTED_FORMATS:
        log.error(f"Input file type with extension {extension} ({path.name}) not supported.")
        raise NotImplementedError

    if extension == constants.MOL2_FORMAT_EXT:
        mol = readMol2File(contents)
        if mol is None:
            log.error(f"Rdkit failed to process file {path.name}.")
            return None
        return mol

    if extension == constants.SMILES_FORMAT_EXT:
        from eMolFrag.input import SmilesReader

        return SmilesReader.readSmilesFile(contents)

    if extension == constants.FASTA_FORMAT_EXT:
        mol = Chem.MolFromFASTA(contents)

    elif extension == constants.YAML_FORMAT_EXT:
        mol = Chem.MolFromHELM(contents)

    elif extension == constants.MOL_FORMAT_EXT:
        mol = Chem.MolFromMolBlock(contents)

    elif extension == constants.PDB_FORMAT_EXT:
        mol = Chem.MolFromPDBBlock(contents)

    elif extension == constants.SMARTS_FORMAT_EXT:
        mol = Chem.MolFromSmarts(contents)

    elif extension == constants.TPL_FORMAT_EXT:
        mol = Chem.MolFromTPLBlock(contents)

    if not mol:
        log.error(f"Molecule file ({path.name}) was not read in due to RDKit Error.")
        return None

    if path:
        log.warning(f"Input file type {extension} ({path.name}) will not preserve molecule SYBL atom types.")
        return mol

    return None


def readMol2File(contents):
    # Turn off rdkit error messages
    # from rdkit import RDLogger
    # RDLogger.DisableLog('rdApp.*')

    # 80 unique bricks among 162 bricks - 11 unique linkers among 78 linkers ||| Chem.MolFromMol2Block(contents)
    # 81 unique bricks among 155 bricks - 10 unique linkers among 75 linkers  ||| Chem.MolFromMol2Block(contents, removeHs=False, cleanupSubstructures=False)
    # 127 unique bricks among 249 bricks - 18 unique linkers among 129 linkers  ||| Chem.MolFromMol2Block(contents, sanitize=False)  ||  SDWriter breaks.
    # 127 unique bricks among 249 bricks - 18 unique linkers among 129 linkers  ||| Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False)  ||  SDWriter breaks.
    # 143 unique bricks among 264 bricks - 18 unique linkers among 137 linkers  ||| Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False, cleanupSubstructures=False)  ||  SDWriter breaks.
    # 0 unique bricks among 0 bricks - 0 unique linkers among 0 linkers ||| Chem.MolFromMol2Block(contents, kekulize=False, sanitize=False)
    # 0 unique bricks among 0 bricks - 0 unique linkers among 0 linkers ||| Chem.MolFromMol2Block(contents, kekulize=False)

    return (
        Chem.MolFromMol2Block(contents) or Chem.MolFromMol2Block(contents, removeHs=False, cleanupSubstructures=False)
        # or Chem.MolFromMol2Block(contents, sanitize=False)
        # or Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False)
        # or Chem.MolFromMol2Block(contents, sanitize=False, removeHs=False, cleanupSubstructures=False)
    )


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
        except Exception as e:
            log.error(f"Error reading file {current_file}: {e}")
            continue
        else:
            # To Mol2Block and Back to Mol Object (to get TriposAtomType)
            # mol = MolToMol2Block(mol)
            # mol = Chem.MolFromMol2Block(mol)
            if mol is None:
                log.warning(f"Molecule {current_file} empty.")
                continue
            if isinstance(mol, list):
                log.debug(f"{mol = }")
                mols += [
                    (
                        Molecule(setAtomTypes(mol), f"{current_file.stem}-{name}")
                        if name and current_file.stem != name
                        else Molecule(setAtomTypes(mol), f"{current_file.stem}")
                    )
                    for name, mol in mol
                ]
            else:
                mols += [Molecule(setAtomTypes(mol), current_file.name)]

    if not mols:
        log.error(f"No molecules generated from files list: {[x.name for x in files]}.")

    return mols


def setAtomTypes(mol):
    # Use _sybyl_atom_type to set atom types
    for idx, atom in enumerate(mol.GetAtoms()):
        mol.GetAtomWithIdx(idx).SetProp("_TriposAtomType", _sybyl_atom_type(atom))

    return mol
