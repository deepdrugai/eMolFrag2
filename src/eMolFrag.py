from eMolFrag2.src.input import MoleculeFileReader, MoleculeReader, Options
from eMolFrag2.src.chopper import Chopper
from eMolFrag2.src.output import writer
from eMolFrag2.src.utilities.logging import log


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

    dataset = []

    # Verify Tools and Parse Command Line

    # Get files
    mol_files = MoleculeFileReader.getFiles(options)
    log.info(f"{len(mol_files)} file{'s'[:len(mol_files)^1]} to be processed.")

    # Get molecules
    molecules = MoleculeReader.getMolecules(mol_files)
    log.info(f"{len(molecules)} molecule{'s'[:len(molecules)^1]} to be chopped.")

    # CHOP
    brick_db, linker_db, fa_db = Chopper.chopall(molecules)

    # Output fragments
    log.info(f"{len(brick_db)} TC-unique bricks among {brick_db.numAllMolecules()} bricks.")
    log.info(f"{len(linker_db)} TC-unique linkers among {linker_db.numAllMolecules()} linkers.")
    log.info(f"{len(fa_db)} TC-unique free atoms among {fa_db.numAllMolecules()} free atoms.")

    writer.write(options, brick_db, linker_db, fa_db, molecules)


if __name__ == "__main__":
    main()
