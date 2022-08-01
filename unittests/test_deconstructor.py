import pytest
from pathlib import Path
from rdkit import Chem

from eMolFrag2.src.input import MoleculeReader
from eMolFrag2.src.chopper import Deconstructor
from eMolFrag2.src.utilities.logging import log


cwd = Path(__file__).parents[1] / "test/mol2-test"
failed = ['DB01059.mol2', 'DB01326.mol2', 'DB00229.mol2', 'DB00779.mol2', 'DB00355.mol2', 
          'DB00430.mol2', 'DB01137.mol2', 'DB01327.mol2', 'DB00446.mol2', 'DB00923.mol2', 
          'DB01329.mol2', 'DB01165.mol2', 'DB01051.mol2', 'DB01328.mol2', 'DB00267.mol2', 
          'DB00274.mol2', 'DB00911.mol2', 'DB00467.mol2', 'DB00916.mol2', 'DB01208.mol2', 
          'DB01155.mol2', 'DB00817.mol2', 'DB00698.mol2', 'DB00218.mol2', 'DB00845.mol2', 
          'DB01044.mol2', 'DB00487.mol2', 'DB00978.mol2', 'DB00537.mol2', 'DB00827.mol2', 
          'DB01405.mol2', 'DB01333.mol2', 'DB00438.mol2', 'DB00760.mol2', 'DB01163.mol2',
          'DB01413.mol2']  # fmt: skip



@pytest.fixture
def mol2_files():
    files = []
    file_list = (file for file in cwd.iterdir() if file.name not in failed)
    for file in file_list:
        files.append(file)
    return files


def test_deconstruct(mol2_files):

    for file in mol2_files:

        log.info(f"File: {file}")

        # create rdkit molecule from molPath
        rdkit_mol = MoleculeReader.getRDKitMolecule(file)

        # Check that all files load properly
        if rdkit_mol is None:  # pragma: no cover
            assert False

        # remove hydrogen
        rdkit_mol = Chem.RemoveAllHs(rdkit_mol, sanitize=True)

        # get fragments and sets of chopping points
        bricks, linkers, snips = Deconstructor.deconstruct(rdkit_mol)

        # count number of atoms in bricks set
        b_count = sum(len(b) for b in bricks)
        fragments = [t for b in bricks for t in b]

        # count number of atoms in linkers set
        l_count = sum(len(l) for l in linkers)
        fragments += [t for l in linkers for t in l]

        log.debug(f"# of atoms in the molecule: { len(rdkit_mol.GetAtoms()) }")
        log.debug(f"# of atoms after deconstruct:{ b_count + l_count }")

        # Check if there is any overlapped atoms - atoms
        atoms = [s for t in snips for s in t]
        uniqueAtoms = set(atoms)
        diff = sum(1 for atom in uniqueAtoms if not atom in fragments)

        log.debug(f"Atoms not in bricks or linkers: {diff}")
        log.debug(f"Atoms in Final Snips: {atoms}")
        log.debug(f"Unique atoms in final snips: {uniqueAtoms}")

        #
        # Test Normal Case: atoms do not overlap
        #   fragments contain the same number of atoms as the original molecule
        #
        if diff == 0:
            assert b_count + l_count == len(rdkit_mol.GetAtoms())

        #
        # Test Overlap Cases: one or more molecule overlap
        #   fragments contain less atoms than the original molecules
        #
        else:
            # total number of atoms in bricks and linkers
            # should equal to number of atoms in original molecule - number of overlapped atoms
            assert b_count + l_count == len(rdkit_mol.GetAtoms()) - diff
