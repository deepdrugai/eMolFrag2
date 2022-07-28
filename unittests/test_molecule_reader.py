import pytest
from pathlib import Path
from eMolFrag2.src.input.MoleculeReader import getMolecules

@pytest.mark.parametrize("input", [
    (["mol2"]),
    (["smi"]),
    (["sdf"]),
    (["pbd"]),
    (["mol"]),
])

#Read files in from unittests/data/db-files for mol2, smi, sdf, pbd, mol (5 tests)
#For each test, if one of those objects returns a None rdkitObject, test fails
def test_get_files(input):
    cwd = Path(__file__).parent / "data/db-files"
    for suffix in input:
        files = []
        file_path = cwd.joinpath(suffix)
        for current_file in file_path.iterdir():
            files.append(file_path / current_file.name)
        mols = getMolecules(files)
        #If any of the returned mols have rdkitObject==None, then the file was not read properly
        assert all(mol.rdkitObject != None for mol in mols)

        # TODO #7 Get SmilesReader.py working, otherwise we have to use the other utilities file to import @wcatykid