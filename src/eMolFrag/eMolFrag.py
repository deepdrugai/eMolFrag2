from eMolFrag.chopper import Chopper
from eMolFrag.input import MoleculeFileReader, MoleculeReader, Options
from eMolFrag.output import writer
from eMolFrag.utilities.logging import log


def main():
    """
    eMolFrag

    (1) Parse input arguments
    (2) Read input files into Molecule objects
    (3) Fragment molecules
    (4) Output fragments as specified by the user

    """
    options = Options.Options()
    # if not options.isRunnable():
    #     log.error(f'Command-line arguments failed to parse; execution of eMolFrag will stop.')
    #     return

    # Verify Tools and Parse Command Line

    # Get files
    mol_files = MoleculeFileReader.getFiles(options)

    if not mol_files:
        log.error(f"No files were found in {options.INPUT_PATH}).")
        return

    mol_files_string = ", ".join([str(m.name) for m in mol_files])
    log.info(f"{len(mol_files)} file{'s'[:len(mol_files) ^ 1]} to be processed: {mol_files_string}.")

    # Get molecules
    molecules = MoleculeReader.getMolecules(mol_files)
    molecules_string = ", ".join([str(m).split(" ")[0] for m in molecules])
    if not molecules:
        log.error(f"No molecules were found in {mol_files_string}.")
        return
    log.info(f"{len(molecules)} molecule{'s'[:len(molecules) ^ 1]} to be chopped: {molecules_string}.")

    # CHOP
    brick_db, linker_db, fa_db, snip_db, og_frag_db = Chopper.chopall(molecules)

    # Output fragments
    log.info(
        f"{len(brick_db)} TC-unique brick{'s'[:len(brick_db) ^ 1]} among {brick_db.numAllMolecules()} brick{'s'[:brick_db.numAllMolecules() ^ 1]}."
    )
    log.info(
        f"{len(linker_db)} TC-unique linker{'s'[:len(linker_db) ^ 1]} among {linker_db.numAllMolecules()} linker{'s'[:linker_db.numAllMolecules() ^ 1]}."
    )
    log.info(
        f"{len(fa_db)} TC-unique freeatom{'s'[:len(fa_db) ^ 1]} among {fa_db.numAllMolecules()} freeatom{'s'[:fa_db.numAllMolecules() ^ 1]}."
    )

    if len(brick_db) == len(linker_db) == len(fa_db) == 0:
        log.error(f"No files were generated from {mol_files}.")
        return

    writer.write(options, brick_db, linker_db, fa_db, snip_db, molecules, og_frag_db)


if __name__ == "__main__":
    main()
