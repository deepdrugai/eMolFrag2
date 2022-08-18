# import shutil
from pathlib import Path

# from eMolFrag2.src.representation import MoleculeDatabase
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.output import stats, draw


def writeMolImgsFromDB(db, out_dir):
    for key, value in db.database.items():
        draw.draw_mol(key.getRDKitObject(), out_dir / (str(key)[: str(key).index(".sdf")] + ".png"))


def prepareDirectory(out_path):
    """
    If the directory does not exist, create it.
    If the directory does exist, clean it.
    """
    if out_path.is_file():
        log.error(f"Output path {str(out_path)} is a file, not a directory.")
        raise ValueError(f"Malformed output specification path {str(out_path)}")

    # Rename the directory, if needed
    new_path = out_path
    i = 1
    while new_path.exists():
        log.warning(f"Output path {str(new_path)} exists; {str(out_path)}-{i} will be used.")
        new_path = out_path.parent / f"{out_path.name}-{i}"
        i += 1
    else:
        log.info(f"Output path {str(new_path)} does not exist; will be created.")

    out_path = new_path
    del new_path, i

    # Create the diretory
    out_path.mkdir()

    # Return new path
    return out_path


def writeSingleFile(indicator, name, out_dir, mols, extension=constants.SDF_FORMAT_EXT):
    """
    indicator --  'u' --> unique or 'a' --> all
    name -- main part of the output file: 'bricks' or 'linkers'
    out_dir -- output directory path
    mols -- the actual Molecule objects to write
    """
    file_name = f"{indicator}{name}{extension}"

    log.debug(f"Writing file {out_dir}/{file_name}")

    # Delimiter needed? Or does SDWriter put it there?
    text = "\n".join([mol.toSDF() for mol in mols])

    out_path = out_dir / file_name

    with out_path.open("w") as f:
        f.write(text)


def writeIndividualFiles(out_dir, mols, extension=constants.SDF_FORMAT_EXT):
    """
    indicator --  'u' --> unique or 'a' --> all
    name -- main part of the output file: 'bricks' or 'linkers'
    out_dir -- output directory path
    mols -- the actual Molecule objects to write
    """
    for mol in mols:
        out_path = out_dir / mol.getFileName()
        with out_path.open("w") as f:
            f.write(mol.toSDF())


def write(options, brick_db, linker_db, molecules=False):
    """
    Main output routine
    The focus is what fragments (unique OR all) and format how to
    output it (many files OR a single file).
    """
    # TODO #21 Draw the input molecules @haydengemeinhardt
    # add molecules to writer

    if molecules:
        # drawing stuff here
        pass

    out_dir = Path(options.OUTPUT_PATH)
    out_dir = prepareDirectory(out_dir)

    log.debug(f"Writing to directory {str(out_dir)}")

    bricks_to_write = []
    linkers_to_write = []
    indicator = ""

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

    # test draw functions
    # brick_dict = [key.getRDKitObject() for key, value in brick_db.database.items()]
    # draw.draw_mol(brick_dict[0], out_dir / 'test1.png')
    # draw.draw_grid_img(brick_dict[0], out_dir / 'test2.svg')
    # draw.draw_grid_img2(brick_dict[0], out_dir / 'test3.svg')
    # draw.highlight_cleave_sights(brick_dict[0], out_dir / 'test4.svg')

    # Draw Images
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)

    writeMolImgsFromDB(brick_db, img_dir)
    writeMolImgsFromDB(linker_db, img_dir)
    stats.histogram(brick_db, linker_db, img_dir)
