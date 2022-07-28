from pathlib import Path
import pytest
from rdkit import Chem
from eMolFrag2.src.utilities.logging import log

#import os
from eMolFrag2.unittests import utilities
from eMolFrag2.src.chopper import Deconstructor

rel_path = "mol2-test"


@pytest.fixture
def kekulize_files():
    k_files = ['DB01328.mol2', 'DB00779.mol2', 'DB01155.mol2',
               'DB00845.mol2', 'DB00430.mol2', 'DB00467.mol2', 'DB01405.mol2',
               'DB01051.mol2', 'DB00537.mol2', 'DB01137.mol2', 'DB00817.mol2',
               'DB00229.mol2', 'DB00487.mol2', 'DB00267.mol2', 'DB01329.mol2',
               'DB00923.mol2', 'DB00218.mol2', 'DB01165.mol2', 'DB01059.mol2',
               'DB01327.mol2', 'DB00274.mol2', 'DB01044.mol2', 'DB01208.mol2',
               'DB00978.mol2', 'DB01326.mol2', 'DB00827.mol2']
    return k_files


def test_deconstruct(kekulize_files):

    for mol_path in kekulize_files:

        cwd = Path(__file__).parents[1] / "test" / rel_path

        #path = cwd / rel_path

        log.debug(f"File path: {cwd}")

        # create rdkit molecule from molPath
        rdkit_mol = utilities.getRDKitMolecule(
            cwd / mol_path, Path(cwd / mol_path).suffix)
        # remove hydrogen
        rdkit_mol = Chem.RemoveAllHs(rdkit_mol, sanitize=True)

        # get fragments and sets of chopping points
        bricks, linkers, snips = Deconstructor.deconstruct(rdkit_mol)

        fragments = []

        # count number of atoms in bricks set
        b_count = 0
        for b in bricks:
            b_count += len(b)
            for t in b:
                fragments.append(t)

        # count number of atoms in linkers set
        l_count = 0
        for l in linkers:
            l_count += len(l)
            for t in l:
                fragments.append(t)

        log.info(f'# of atoms in the molecule: { len(rdkit_mol.GetAtoms()) }')
        log.info(f'# of atoms after deconstruct:{ b_count + l_count }')

        # Check if there is any overlapped atoms - atoms
        atoms = []
        for s in snips:
            atoms += s

        uniqueAtoms = set(atoms)

        diff = 0
        for atom in uniqueAtoms:
            if not atom in fragments:
                diff += 1

        log.info(f'Atoms not in bricks or linkers: {diff}')

        # difference = len(atoms) - len(uniqueAtoms)
        log.info(f'Atoms in Final Snips: {atoms}')
        log.info(f'Unique atoms in final snips: {uniqueAtoms}')

        #
        # Test Normal Case: atoms do not overlap
        #   fragments contain the same number of atoms as the original molecule
        #
        if diff == 0:
            # print("Running Normal Tests")
            assert b_count + l_count == len(rdkit_mol.GetAtoms())

        #
        # Test Overlap Cases: one or more molecule overlap
        #   fragments contain less atoms than the original molecules
        #
        else:
            # total number of atoms in bricks and linkers
            #      should equal to number of atoms in original molecule - number of overlapped atoms
            # print("Running Tests with Overlapped Atoms")
            assert b_count + l_count == len(rdkit_mol.GetAtoms()) - diff
