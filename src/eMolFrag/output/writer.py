# import shutil
from pathlib import Path

from rdkit.Chem import MolToSmiles

from eMolFrag.output import draw, stats, trace
from eMolFrag.output import networktext as nt
from eMolFrag.utilities import constants

# from eMolFrag.representation import MoleculeDatabase
from eMolFrag.utilities.logging import log


def writeMolImgsFromDB(db, out_dir, filetype=".png"):
    # log.debug(f"{db = }")
    # log.debug(f"{db.database = }")
    # log.debug(f"{db.database.items() = }")
    # log.debug(f"{db.GetAllMolecules() = }")
    for mol in db.GetAllMolecules():
        rdkitmol = mol.getRDKitObject()
        fragname = Path(mol.filename).stem
        # log.debug(f"{fragname = }\t{rdkitmol = }")
        draw.draw_mol(rdkitmol, out_dir / (fragname + filetype))  # Valid choices are pdf, svg, ps, and png


def prepareDirectory(out_path):
    """
    If the directory does not exist, create it.
    If the directory does exist, clean it.
    """
    if out_path.is_file():
        log.error(f"Output path {out_path!s} is a file, not a directory.")
        raise ValueError(f"Malformed output specification path {out_path!s}")

    # Rename the directory, if needed
    new_path = out_path
    i = 1
    while new_path.exists():
        log.warning(f"Output path {new_path} exists; Trying {out_path!s}-{i}.")
        new_path = out_path.parent / f"{out_path.name}-{i}"
        i += 1
    log.debug(f"Output path {new_path.resolve()} does not exist, will be created.")

    out_path = new_path
    del new_path, i

    # Create the diretory
    out_path.mkdir(parents=True)

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


def writeIndividualFiles(out_dir, mols):
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


def writeTraceFiles(out_dir, snip_db, mols, extension=constants.TRACE_FORMAT_EXT):
    """
    Write trace (reconstruction) files.
    snip_db -- Snip database
    out_dir -- output directory path
    mols -- the actual Molecule objects to write
    """
    for mol in mols:
        fname = f"t-{mol.getFileName()}{extension}"
        out_path = out_dir / fname
        log.debug(f"Writing trace to {out_path}")

        with out_path.open("a") as f:
            # Mol Name
            f.write("# " + mol.getFileName() + "\t(" + fname + ")\n")
            f.write("\n")

            # generate network text
            mol_nx = trace.mol_to_nx(mol.getRDKitObject())
            nt.write_network_text(mol_nx, with_labels="atom_symbol", path=f)
            f.write("\n" * 2)

            # write snips
            for snipa, snipb in snip_db[mol.getFileName()]:
                f.write(str(snipa) + "\t" + str(snipb) + "\n")
            f.write("\n")

            # write smiles target
            f.write("target:\t" + MolToSmiles(mol.getRDKitObject()) + "\n")


def write(options, brick_db, linker_db, fa_db, snip_db, molecules):
    """
    Main output routine
    The focus is what fragments (unique OR all) and format how to
    output it (many files OR a single file).
    """

    out_dir = Path(options.OUTPUT_PATH)
    out_dir = prepareDirectory(out_dir)

    log.info(f"Writing to directory {out_dir.resolve()}")

    bricks_to_write = []
    linkers_to_write = []
    fa_to_write = []

    indicator = ""

    # All fragments wanted
    if options.ALL_FRAGMENTS:
        indicator = constants.FILE_OUTPUT_ALL_INDICATOR
        bricks_to_write = brick_db.GetAllMolecules()
        linkers_to_write = linker_db.GetAllMolecules()
        fa_to_write = fa_db.GetAllMolecules()

    # Only unique fragments wanted
    else:
        indicator = constants.FILE_OUTPUT_UNIQUE_INDICATOR
        bricks_to_write = brick_db.GetUniqueMolecules()
        linkers_to_write = linker_db.GetUniqueMolecules()
        fa_to_write = fa_db.GetUniqueMolecules()

    # Write all fragments to their own files
    if options.INDIVIDUAL:
        writeIndividualFiles(out_dir, bricks_to_write + linkers_to_write + fa_to_write)

    # Write all fragments to a single brick and a signle linker file
    else:
        writeSingleFile(indicator, constants.BRICK_SINGLE_FILE_OUTPUT_NAME, out_dir, bricks_to_write)
        writeSingleFile(indicator, constants.LINKER_SINGLE_FILE_OUTPUT_NAME, out_dir, linkers_to_write)
        writeSingleFile(indicator, constants.FREEATOM_SINGLE_FILE_OUTPUT_NAME, out_dir, fa_to_write)

    # test draw functions
    # brick_dict = [key.getRDKitObject() for key, value in brick_db.database.items()]
    # draw.draw_mol(brick_dict[0], out_dir / 'test1.png')
    # draw.draw_grid_img(brick_dict[0], out_dir / 'test2.svg')
    # draw.draw_grid_img2(brick_dict[0], out_dir / 'test3.svg')
    # draw.highlight_cleave_sights(brick_dict[0], out_dir / 'test4.svg')

    # Create Trace File
    if options.TRACE:
        # for mol in molecules:
        # log.error(f"{mol.getFileName()}'s snips: {snip_db[mol.getFileName()]}")
        writeTraceFiles(out_dir, snip_db, molecules)
        # log.error("Hi, this is the drawn trace output tree.")
        # trace.example()

    # Draw Images
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)

    writeMolImgsFromDB(brick_db, img_dir)
    writeMolImgsFromDB(linker_db, img_dir)
    writeMolImgsFromDB(fa_db, img_dir)
    stats.histogram(brick_db, linker_db, img_dir)
