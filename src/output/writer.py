import shutil
from pathlib import Path

from SuperSecretProject.src.representation import MoleculeDatabase
from SuperSecretProject.src.utilities import logging
from SuperSecretProject.src.utilities import constants

def prepareDirectory(out_path):
    """
        If the directory does not exist, create it.
        If the directory does exist, clean it.        
    """
    if out_path.is_file():
        logging.logger.error(f'Output path {str(out_path)} is a file, not a directory.')
        raise ValueError(f'Malformed output specification path {str(out_path)}')

    # Rename the directory, if needed    
    new_path = out_path
    i=1
    while new_path.exists():
        logging.logger.warning(f'Output path {str(new_path)} exists; {str(out_path)}-{i} will be used.')
        new_path = out_path.parent / f"{out_path.name}-{i}"
        i+=1
    else:
        logging.logger.info(f'Output path {str(new_path)} does not exist; will be created.')

    out_path = new_path
    del new_path, i
    
    # Create the diretory
    out_path.mkdir()

    # Return new path
    return out_path

def writeSingleFile(indicator, name, out_dir, mols, extension = constants.SDF_FORMAT_EXT):
    """
        indicator --  'u' --> unique or 'a' --> all
        name -- main part of the output file: 'bricks' or 'linkers'
        out_dir -- output directory path
        mols -- the actual Molecule objects to write
    """
    file_name = f'{indicator}{name}{extension}'

    logging.logger.debug(f'Writing file {out_dir}/{file_name}')

    # Delimiter needed? Or does SDWriter put it there?
    text = '\n'.join([mol.toSDF() for mol in mols])

    out_path = out_dir / file_name

    with out_path.open('w') as f:
            f.write(text)

def writeIndividualFiles(out_dir, mols, extension = constants.SDF_FORMAT_EXT):
    """
        indicator --  'u' --> unique or 'a' --> all
        name -- main part of the output file: 'bricks' or 'linkers'
        out_dir -- output directory path
        mols -- the actual Molecule objects to write
    """
    for mol in mols:    
        out_path = out_dir / mol.getFileName()
        with out_path.open('w') as f:
            f.write(mol.toSDF())

def write(options, brick_db, linker_db):
    """
        Main output routine
        The focus is what fragments (unique OR all) and format how to
        output it (many files OR a single file).
    """
    out_dir = Path(options.OUTPUT_PATH)
    out_dir = prepareDirectory(out_dir)

    logging.logger.debug(f'Writing to directory {str(out_dir)}')

    bricks_to_write = []
    linkers_to_write = []
    indicator = ''

    # All fragments wanted
    if options.ALL_FRAGMENTS:
        indicator = constants.FILE_OUTPUT_ALL_INDICATOR
        bricks_to_write = brick_db.GetAllMolecules()
        linkers_to_write = linker_db.GetAllMolecules()
        
    # Only unique fragments wanted
    else:
        indicator = constants.FILE_OUTPUT_UNIQUE_INDICATOR
        bricks_to_write = brick_db.GetUniqueMolecules()
        linkers_to_write = linker_db.GetUniqueMolecules()

    # Write all fragments to their own files
    if options.INDIVIDUAL:
        writeIndividualFiles(out_dir, bricks_to_write + linkers_to_write)

    # Write all fragments to a single brick and a signle linker file
    else:
        writeSingleFile(indicator, constants.BRICK_SINGLE_FILE_OUTPUT_NAME, out_dir, bricks_to_write)
        writeSingleFile(indicator, constants.LINKER_SINGLE_FILE_OUTPUT_NAME, out_dir, linkers_to_write)