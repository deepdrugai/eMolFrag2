import pytest
from pathlib import Path

from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.chopper import Chopper
from eMolFrag2.src.input.MoleculeReader import to_mol

cwd = Path(__file__).parent / "data/9070-non-c2-c2-double-bond"


@pytest.fixture
def output():
    expectedLinks = ["l-CHEMBL9070.mol2-000.sdf"]

    expectedBricks = [
        "b-CHEMBL9070.mol2-000.sdf",
        "b-CHEMBL9070.mol2-001.sdf",
        "b-CHEMBL9070.mol2-002.sdf",
        "b-CHEMBL9070.mol2-003.sdf",
        "b-CHEMBL9070.mol2-004.sdf",
    ]
    return expectedBricks, expectedLinks


@pytest.mark.parametrize("input", [[to_mol(cwd / "CHEMBL9070.mol2")]])
def test_chopall(input, output):
    # get bricks and linkers from input
    bricks, links = Chopper.chopall(input)
    eBrick, eLink = output
    log.info(f"{[x for x in bricks.GetAllMolecules()] = }")
    log.info(f"{links.GetAllMolecules() = }")
    log.info(f"{eBrick = }, {eLink = }")
    # compare if expected links are equal to actual links
    for line in links.GetAllMolecules():
        log.info(f"links {line = }")
        assert eLink.__contains__(line.toSDF()[0:25])

    # compare if expected bricks are equal to actual bricks
    for line in bricks.GetAllMolecules():
        log.info(f"bricks {line = }")
        assert eBrick.__contains__(line.toSDF()[0:25])
