import pytest
from pathlib import Path
from rdkit import Chem

from eMolFrag2.src.input import MoleculeReader
from eMolFrag2.src.chopper import Deconstructor
from eMolFrag2.src.utilities.logging import log


cwd = Path(__file__).parents[1] / "test/mol2-test"

@pytest.fixture
def mol2_files():
    files = []
    for file in cwd.iterdir():
        files.append(file)
    return files


def test_deconstruct(mol2_files):

    for file in mol2_files:
        # file_path = cwd / mol_path

        log.info(f"File: {file}")

        # create rdkit molecule from molPath
        rdkit_mol = MoleculeReader.getRDKitMolecule(file)

        if rdkit_mol is None:
            # assert False
            continue

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

        log.debug(f'# of atoms in the molecule: { len(rdkit_mol.GetAtoms()) }')
        log.debug(f'# of atoms after deconstruct:{ b_count + l_count }')

        # Check if there is any overlapped atoms - atoms
        atoms = [s for t in snips for s in t]
        uniqueAtoms = set(atoms)
        diff = sum(1 for atom in uniqueAtoms if not atom in fragments)

        log.debug(f'Atoms not in bricks or linkers: {diff}')
        log.debug(f'Atoms in Final Snips: {atoms}')
        log.debug(f'Unique atoms in final snips: {uniqueAtoms}')

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
