from pathlib import Path

from rdkit import Chem
from rdkit import RDLogger

from eMolFrag2.src.representation import Molecule
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.utilities.logging import log

# TODO: move to utilities
def fileToString(file):
    """
        Read the entire contents of a file into a string

        @input: file -- valid path to a file
    """
    contents = ""
    with open(file) as f:
        contents = f.read()

    return contents

def getRDKitMolecule(path, extension=None):
    """
        Given a path object, return the corresponding RDKit molecule object
        This simplified functionality is for testing only
    """
    if extension is None:
       extension = Path(path).suffix
    content = fileToString(path)
    return convertToRDkit(content, extension)

def convertToRDkit(contents, curr_file):
    """
        Attempt to read and convert the input file into an RdKit.Mol object
        
        @input: contents -- string contents of a file
        @input: mol)file -- input molecule file name
        
        @output: list of tuples: [(id, rdkit_mol)]
    """
    #Chem.doKekule = False

    extension = curr_file.suffix

    if (extension == constants.MOL2_FORMAT_EXT):
        mol = readMol2File(contents)
        if mol is None:
            log.error(f'Rdkit failed to process mol2 file {curr_file.name}')
            return None
        return [(curr_file.name, mol)]

    elif (extension == constants.SMILES_FORMAT_EXT):
        from eMolFrag2.src.input import SmilesReader
        return SmilesReader.readSmilesFile(contents)

    #
    # Other file formats that do not support AtomTypes
    #
    mol = None    

    if (extension == constants.FASTA_FORMAT_EXT):
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

    else:
        log.error(f'Input file type with extension {extension} not supported.')

    if mol is not None:
        log.warning(f'Input file type {extension} will not preserve molecule SYBL atom types')
        return [(curr_file.name, mol)]

    return None

def readMol2File(contents):
    # Turn off rdkit error messages 
    RDLogger.DisableLog('rdApp.*')

    try: 
        return Chem.MolFromMol2Block(contents)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, kekulize = False)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, kekulize = False, sanitize = False)
    except:
        pass
    try: 
         return Chem.MolFromMol2Block(contents, sanitize = False)
    except:
        pass
    try: 
        return Chem.MolFromMol2Block(contents, sanitize = False, removeHs = False)
    except: 
        pass
    try: 
        return Chem.MolFromMol2Block(contents, sanitize = False, removeHs = False, cleanupSubstructures = False)
    except: 
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
        id_mol_list = None
        try:
            id_mol_list = convertToRDkit(file_contents, current_file)
        except:
            log.error(f'RDKit failed to read {current_file.name}', exc_info=True)

        # add it to our dataset and update the filenames we have
        if id_mol_list is not None:
            for mol_id, mol in id_mol_list:
                mols.append(Molecule.Molecule(mol, mol_id))
   
    return mols