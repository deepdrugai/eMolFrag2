import pytest
import sys
from pathlib import Path
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.input import Options, MoleculeFileReader

@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [5]),
    (["sdf"], [0]),
    (["pbd"], [5]),
    (["mol"], [5]),
])

def test_get_files(input, expected):
    cwd = Path(__file__).parent / "data/db-files"
    for m, e in zip(input, expected):
        filePath = Path(__file__).parent.joinpath("config.emf")
        sys.argv = ['eMolFrag2/src/eMolFrag.py', '-i', str(cwd/m), '-o', '/content/out']
        options = Options.Options()
        assert len(MoleculeFileReader.getFiles(options)) == e
