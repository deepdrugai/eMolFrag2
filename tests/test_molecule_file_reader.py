import pytest
import sys
from pathlib import Path
from eMolFrag.utilities.logging import log
from eMolFrag.input import Options, MoleculeFileReader

data = Path(__file__).parent.parent / "data"
dir = data / "db-files"

@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [5]),
    (["sdf"], [0]),
    (["pbd"], [4]),
    (["mol"], [5]),
    (["path_not_exists"], [0]), #test if directory doesn't exist
    (["mol/DB00415.mol"], [1]), #test if not a directory
])  # fmt: skip


def test_get_files(input, expected):
    for m, e in zip(input, expected):
        sys.argv = ["emolfrag", "-i", str(dir / m), "-o", "/content/out"]
        options = Options.Options()
        assert len(MoleculeFileReader.getFiles(options)) == e
