import pytest
from pathlib import Path
from itertools import product

from rdkit.DataStructs import FingerprintSimilarity
from rdkit.Chem import SDMolSupplier, RDKFingerprint

from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.chopper.Chopper import chopall
from eMolFrag2.src.input.MoleculeReader import to_mol


dir = Path(__file__).parent / "data/chopper"


@pytest.mark.parametrize("cwd, cwdex", [(dir / f"mol2-{n}", dir / f"mol2-{n}-out") for n in range(1, 4)])
def test_chopall(cwd, cwdex):

    elinks = [file for file in cwdex.iterdir() if str(file.name).startswith("l-")]
    ebricks = [file for file in cwdex.iterdir() if str(file.name).startswith("b-")]
    elinks = [SDMolSupplier(str(cwdex / x)) for x in elinks]
    ebricks = [SDMolSupplier(str(cwdex / x)) for x in ebricks]

    input = [file for file in cwd.iterdir()]
    bricks, links, freeatoms = chopall([to_mol(x) for x in input])
    links = [x.getRDKitObject() for x in links.GetAllMolecules()]
    bricks = [x.getRDKitObject() for x in bricks.GetAllMolecules()]

    linker_tc = []
    for sdf_set in elinks:
        mols = [mol for mol in sdf_set if mol is not None]

        for x, y in list(product(links, mols)):
            fp_x = RDKFingerprint(x)
            fp_y = RDKFingerprint(y)
            tc = FingerprintSimilarity(fp_x, fp_y)

            if tc > 0.999:
                linker_tc.append((x, y, tc))

    brick_tc = []
    for sdf_set in ebricks:
        mols = [mol for mol in sdf_set if mol is not None]

        for x, y in list(product(bricks, mols)):
            fp_x = RDKFingerprint(x)
            fp_y = RDKFingerprint(y)
            tc = FingerprintSimilarity(fp_x, fp_y)

            if tc > 0.999:
                brick_tc.append((x, y, tc))

    log.debug(f"{len(linker_tc) = } == {len(links) = } is {len(linker_tc) == len(links)}")
    log.debug(f"{len(brick_tc) = } == {len(bricks) = } is {len(brick_tc) == len(bricks)}")

    assert len(brick_tc) == len(bricks)
    assert len(linker_tc) == len(links)
