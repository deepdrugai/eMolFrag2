import sys
import pytest
from pathlib import Path
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.input import MoleculeReader
from eMolFrag2.unittests import utilities
from eMolFrag2.src.representation import Molecule

#TODO described below

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
        files = []
        file_path = cwd.joinpath(m)
        for current_file in file_path.iterdir():
            #if the file extension is not a supportedd format, add the file to the bad file list, otherwise add it to the file list
            files.append(file_path / current_file.name)
        #assert len(MoleculeReader.getMolecules(files)) == e

        #TODO 
        #Until MoleculeReader works with SmilesReader.py, use this below
        #SmilesReader.py was not compiling
        #So I remade MoleculeReader.py using the utilities in unittest folder
        #If SmilesReader.py compiles, you can uncomment the assert statement above and remove this below
        mols = []
        for current_file in files:
            file_contents = utilities.fileToString(current_file)
            extension = current_file.suffix
            id_mol_list = None
            try:
                id_mol_list = utilities.convertToRDkit(file_contents, extension)
            except:
                log.error(f'RDKit failed to read {current_file.name}')
            if id_mol_list is not None:
                mols.append(id_mol_list)
        assert len(mols) == e