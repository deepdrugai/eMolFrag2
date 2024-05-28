import sys
from pathlib import Path

import pytest
from eMolFrag.input import MoleculeFileReader, Options

data = Path(__file__).parent.parent / "data"
datadir = data / "db-files"


@pytest.mark.parametrize(("suffix", "count"), [
    ("mol2", 5),
    ("smi", 5),
    ("sdf", 0),
    ("pbd", 4),
    ("mol", 5),
    ("path_not_exists", 0),  # test if directory doesn't exist
    ("mol/DB00415.mol", 1),  # test if not a directory
])  # fmt: skip
def test_get_files(suffix, count):
    sys.argv = ["emolfrag", "-i", str(datadir / suffix), "-o", "/content/out"]
    options = Options.Options()
    assert len(MoleculeFileReader.getFiles(options)) == count
