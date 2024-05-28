from pathlib import Path

import pytest
from eMolFrag.input.MoleculeReader import getMolecules, to_mol
from eMolFrag.utilities.logging import log

data = Path(__file__).parent.parent / "data"
datadir = data / "db-files"
failed_mol_path = data / "testdata/mol2-test"


@pytest.mark.parametrize("suffix", [
    "mol2",
    "smi",
    pytest.param("sdf", marks=pytest.mark.xfail(raises=NotImplementedError)),
    "pbd",
    "mol",
    "failed"
])  # fmt: skip
def test_to_mol(suffix):  # single file to mol
    file_path = datadir.joinpath(suffix)
    if suffix == "failed":  # testing for a failed mol that has a supported format
        failed_mol = to_mol(failed_mol_path / "DB01059.mol2")
        assert failed_mol.rdkitObject is None
    else:
        for current_file in file_path.iterdir():
            mol = to_mol(current_file)  # Directly pass current_file which already includes the path

            # Testing for unsupported format
            assert mol.rdkitObject is not None if suffix != "sdf" else mol.rdkitObject is None


@pytest.mark.parametrize(("suffix", "expected"), [
    ("mol2", 5),
    ("smi", 6),
    ("sdf", 0),
    ("pbd", 4),
    ("mol", 5),
    ("failed", 0)
])  # fmt: skip
def test_get_files(suffix, expected):  # multiple files to mol
    files = []
    if suffix == "failed":
        failed_mols = ["DB01059.mol2", "DB01326.mol2", "DB00229.mol2", "DB00779.mol2", "DB00430.mol2"]
        files = [failed_mol_path / file for file in failed_mols]
    else:
        file_path = datadir.joinpath(suffix)
        files = [file_path / f.name for f in file_path.iterdir()]

    mols = getMolecules(files)
    log.debug(mols)

    assert len(mols) == expected

    if suffix != "sdf":  # Unsupported format should return an empty list or None in mol objects
        assert all(mol.rdkitObject is not None for mol in mols)
