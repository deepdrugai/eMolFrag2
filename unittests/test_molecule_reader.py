import pytest
from pathlib import Path
from eMolFrag2.src.input.MoleculeReader import getMolecules, to_mol
from eMolFrag2.src.utilities.logging import log

cwd = Path(__file__).parent / "data/db-files"
failed_mol_path = Path(__file__).parent.parent /"test/mol2-test"

failed_mol_path = Path(__file__).parent.parent / "test/mol2-test"
@pytest.mark.parametrize("input", [
    (["mol2"]),
    (["smi"]),
    (pytest.param(["sdf"],marks=pytest.mark.xfail(raises=NotImplementedError))),
    (["pbd"]),
    (["mol"]),
    (["failed"]),
])  # fmt: skip
def test_to_mol(input):  # single file to mol
    for suffix in input:
        file_path = cwd.joinpath(suffix)
        if suffix == "failed": #testing for a failed mol that has a supported format
            failed_mol = to_mol(failed_mol_path /"DB01059.mol2")
            assert failed_mol.rdkitObject == None
        else:  # checking if all mols in supported format test folders return a conversion
            for current_file in file_path.iterdir():
                mol = to_mol(file_path / current_file)

                # tesing for an unsupported format
                assert mol.rdkitObject == None if suffix == ("sdf") else mol.rdkitObject != None


@pytest.mark.parametrize("input, expected", [
    (["mol2"], [5]),
    (["smi"], [6]),
    (["sdf"], [0]),
    (["pbd"], [4]),
    (["mol"], [5]),
    (["failed"], [0])
])
def test_get_files(input, expected): #multiple files to mol
    failed_mols = ['DB01059.mol2', 'DB01326.mol2', 'DB00229.mol2', 'DB00779.mol2', 'DB00355.mol2', 'DB00430.mol2'] 

    for suffix, e in zip(input, expected):
        files = []
        if suffix == "failed":
            for file in failed_mols:
                files.append(failed_mol_path / file)
            mols = getMolecules(files)
            assert len(mols) == e
        else:
            file_path = cwd.joinpath(suffix)
            for current_file in file_path.iterdir():
                files.append(file_path / current_file.name)
            mols = getMolecules(files)
            log.debug(mols)
            
            # Assert that length of mols == e
            assert len(mols) == e
            
            if not suffix == "sdf": #unsupported format, so should return an empty list
                #If any of the returned mols have rdkitObject==None, then the file was not read properly
                assert all(mol.rdkitObject != None for mol in mols)
            # Assert that length of mols == e
            assert len(mols) == e

            if not suffix == "sdf":  # unsupported format, so should return an empty list
                # If any of the returned mols have rdkitObject==None, then the file was not read properly
                assert all(mol.rdkitObject != None for mol in mols)
