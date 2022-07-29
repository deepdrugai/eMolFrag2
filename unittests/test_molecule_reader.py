import pytest
from pathlib import Path
from eMolFrag2.src.input.MoleculeReader import getMolecules, to_mol
from eMolFrag2.src.utilities.logging import log

cwd = Path(__file__).parent / "data/db-files"

@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [5]),
    (["sdf"], [0]),
    (["pbd"], [4]),
    (["mol"], [5]),
])

#Read files in from unittests/data/db-files for mol2, smi, sdf, pbd, mol (5 tests)
#For each test, if one of those objects returns a None rdkitObject, test fails
def test_get_files(input, expected):
    for suffix, e in zip(input, expected):
        files = []
        file_path = cwd.joinpath(suffix)
        for current_file in file_path.iterdir():
            files.append(file_path / current_file.name)
        mols = getMolecules(files)
        #If any of the returned mols have rdkitObject==None, then the file was not read properly
        assert all(mol.rdkitObject != None for mol in mols) and len(mols) == e

        # TODO #7 Get SmilesReader.py working, otherwise we have to use the other utilities file to import @wcatykid

@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [5]),
    (["sdf"], [0]),
    (["pbd"], [5]),
    (["mol"], [5]),
])
def test_to_mol(input, expected):
    for suffix, e in zip(input, expected):
        mols = []
        file_path = cwd.joinpath(suffix)
        for current_file in file_path.iterdir():
            #files.append(file_path / current_file.name)
            mols.append(to_mol(file_path / current_file))
        # for file in files:
        #     mols = to_mol(file)
        #If any of the returned mols have rdkitObject==None, then the file was not read properly
        log.debug(mols)
        assert all(mol.rdkitObject != None for mol in mols) and len(mols) == e