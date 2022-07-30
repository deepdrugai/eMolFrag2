import pytest
from pathlib import Path
from eMolFrag2.src.input.MoleculeReader import getMolecules, to_mol
from eMolFrag2.src.utilities.logging import log

cwd = Path(__file__).parent / "data/db-files"

#Read files in from unittests/data/db-files for mol2, smi, sdf, pbd, mol (5 tests)
#For each test, if one of those objects returns a None rdkitObject, test fails

@pytest.mark.parametrize("input", [
    (["mol2"]),
    (["smi"]),
    (["sdf"]),
    (["pbd"]),
    (["mol"]),
    (["failed"])
])
def test_to_mol(input): #single file to mol
    for suffix in input:
        file_path = cwd.joinpath(suffix)
        if suffix == "failed": #testing for a failed mol that has a supported format
            failed_mol = to_mol(Path(__file__).parent.parent /"test/mol2-test/DB01059.mol2")
            assert failed_mol.rdkitObject == None
        else: #checking if all mols in supported format test folders return a conversion
            for current_file in file_path.iterdir():
                mol = to_mol(file_path / current_file)
                if suffix == "sdf": #tesing for an unsupported format
                    assert mol.rdkitObject == None
                else:
                    assert mol.rdkitObject != None


@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [5]),
    (["sdf"], [0]),
    (["pbd"], [5]),
    (["mol"], [5]),
])
def test_get_files(input, expected): #multiple files to mol
    for suffix, e in zip(input, expected):
        files = []
        file_path = cwd.joinpath(suffix)
        for current_file in file_path.iterdir():
            files.append(file_path / current_file.name)
        mols = getMolecules(files)
        log.debug(mols)
        if suffix == "sdf": #unsupported format, so should return an empty list
            assert len(mols) == e
        #If any of the returned mols have rdkitObject==None, then the file was not read properly
        else:
            assert all(mol.rdkitObject != None for mol in mols) and len(mols) == e

        # TODO #7 Get SmilesReader.py working, otherwise we have to use the other utilities file to import @wcatykid



#test nonexistent file, test direct instead of file, test failed mol2s?