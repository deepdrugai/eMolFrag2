from pathlib import Path

import pytest
from eMolFrag.input.MoleculeReader import to_mol
from eMolFrag.representation.MoleculeDatabase import MoleculeDatabase
from eMolFrag.utilities.logging import log

data = Path(__file__).parent.parent / "data"


@pytest.fixture
def tc1_mol_pairs():
    ms = [("similarPairSMI/1/DB00452.smi", "similarPairSMI/1/DB01421.smi"),
          ("similarPairSMI/2/DB01137.smi", "similarPairSMI/2/DB01165.smi"),
          ("similarPairSMI/3/DB12447.smi", "similarPairSMI/3/DB16219.smi"),]  # fmt: skip
    molpairs = []

    for a, b in ms:
        am = to_mol(data / a)
        bm = to_mol(data / b)
        molpairs.append([am, bm])
    return molpairs


@pytest.fixture
def five_mols():
    ms = ["uniqueMol(SMI)/DB00415.smi",
          "uniqueMol(SMI)/DB01208.smi",
          "uniqueMol(SMI)/DB04626.smi",
          "uniqueMol(SMI)/DB11774.smi",
          "uniqueMol(SMI)/DB13499.smi",]  # fmt: skip
    mols = []

    for m in ms:
        mols.append(to_mol(data / m))
    return mols


@pytest.mark.parametrize("input, expected", [
    # Single Molecules
    (["similarPairSMI/3/DB12447.smi"], [True]),
    (["similarPairSMI/3/DB16219.smi"], [True]),
    # Same molecule
    (["similarPairSMI/3/DB12447.smi", "similarPairSMI/3/DB12447.smi"], [True, False]),
    # Two molecules of TC = 1.0
    (["similarPairSMI/3/DB12447.smi", "similarPairSMI/3/DB16219.smi"], [True, False]),
    # Five Molecules with tc < 1.0
    (["uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi",
      "uniqueMol(SMI)/DB04626.smi", "uniqueMol(SMI)/DB11774.smi",
      "uniqueMol(SMI)/DB13499.smi"], [True] * 5),
])  # fmt: skip
def test_add_mol_to_mdb(input, expected, tc=1.0):
    """Test adding TC Equivalent molecules to Molecule Database where given_tc = 1"""

    mdb = MoleculeDatabase(given_tc=tc)

    for m, e in zip(input, expected):
        log.debug(f"{data / m}\t{e}")
        assert mdb.add(to_mol(data / m)) is e


def test_add_list_to_mdb(five_mols, tc=1.0):
    """Test adding a list to molecule database"""
    mdb = MoleculeDatabase(tc)
    log.debug(f"{len(five_mols) = }")
    assert len(mdb.addAll(five_mols)) == len(five_mols)


def test_length_unique_molecules_mdb(five_mols, tc1_mol_pairs):
    """Test adding a large number of mols to molecules database and get unique"""

    mdb1 = MoleculeDatabase(given_tc=1.0)

    # Test 1: Adding 5 unique molecules to mdb1
    mdb1.addAll(five_mols)
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1) == 5

    # Test 2: Add pairs of similar molecules (tc = 1.0) to mdb1
    mdb1.addAll(tc1_mol_pairs[0])
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1) == 6

    # Test 3: add 2nd pair of similar molecules to mdb1
    mdb1.addAll(tc1_mol_pairs[1])
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1) == 7

    # Test 4: add 3 sets of 2 similar molecules to mdb2
    mdb2 = MoleculeDatabase()
    mdb2.addAll([x for xs in tc1_mol_pairs for x in xs])
    log.debug(f"{len(mdb2) = }")
    assert len(mdb2) == 3

    # Test 5: create a new database and add all 11 molecules at once
    mdb3 = MoleculeDatabase()
    mdb3.addAll([x for xs in tc1_mol_pairs for x in xs] + five_mols)
    log.debug(f"{len(mdb3) = }")
    assert len(mdb3) == 8


def test_get_all_molecules_mdb(five_mols, tc1_mol_pairs):
    """Test adding a large number of mols to molecules database and get total molecules"""

    mdb1 = MoleculeDatabase(given_tc=1.0)

    # Test 1: Adding 5 unique molecules to mdb1
    mdb1.addAll(five_mols)
    log.debug(f"{len(mdb1) = }, {mdb1.numAllMolecules() = }")
    assert mdb1.numAllMolecules() == 5

    # Test 2: Add pairs of similar molecules (tc = 1.0) to mdb1
    mdb1.addAll(tc1_mol_pairs[0])
    log.debug(f"{len(mdb1) = }, {mdb1.numAllMolecules() = }")
    assert mdb1.numAllMolecules() == 7

    # Test 3: add 2nd pair of similar molecules to mdb1
    mdb1.addAll(tc1_mol_pairs[1])
    log.debug(f"{len(mdb1) = }, {mdb1.numAllMolecules() = }")
    assert mdb1.numAllMolecules() == 9

    # Test 4: add 3 sets of 2 similar molecules to mdb2
    mdb2 = MoleculeDatabase()
    mdb2.addAll([x for xs in tc1_mol_pairs for x in xs])
    log.debug(f"{len(mdb2) = }, {mdb2.numAllMolecules() = }")
    assert mdb2.numAllMolecules() == 6

    # Test 5: create a new database and add all 11 molecules at once
    mdb3 = MoleculeDatabase()
    mdb3.addAll([x for xs in tc1_mol_pairs for x in xs] + five_mols)
    log.debug(f"{len(mdb3) = }, {mdb3.numAllMolecules() = }")
    assert mdb3.numAllMolecules() == 11


def test_get_uniq_molecules_mdb(five_mols, tc1_mol_pairs):
    """Test adding a large number of mols to molecules database and get unique"""

    mdb1 = MoleculeDatabase(given_tc=1.0)

    # Test 1: Adding 5 unique molecules to mdb1
    mdb1.addAll(five_mols)
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1.GetUniqueMolecules()) == 5

    # Test 2: Add pairs of similar molecules (tc = 1.0) to mdb1
    mdb1.addAll(tc1_mol_pairs[0])
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1.GetUniqueMolecules()) == 6

    # Test 3: add 2nd pair of similar molecules to mdb1
    mdb1.addAll(tc1_mol_pairs[1])
    log.debug(f"{len(mdb1) = }")
    assert len(mdb1.GetUniqueMolecules()) == 7

    # Test 4: add 3 sets of 2 similar molecules to mdb2
    mdb2 = MoleculeDatabase()
    mdb2.addAll([x for xs in tc1_mol_pairs for x in xs])
    log.debug(f"{len(mdb2) = }")
    assert len(mdb2.GetUniqueMolecules()) == 3

    # Test 5: create a new database and add all 11 molecules at once
    mdb3 = MoleculeDatabase()
    mdb3.addAll([x for xs in tc1_mol_pairs for x in xs] + five_mols)
    log.debug(f"{len(mdb3) = }")
    assert len(mdb3.GetUniqueMolecules()) == 8

    log.debug(f"{str(mdb1) = !s}")
    log.debug(f"{str(mdb2) = !s}")
    log.debug(f"{str(mdb3) = !s}")


def test_mdb_fail():
    # TODO: This needs to not be a RuntimeError, but a more specific error, otherwise other errors (like file read errors) can cause this test to pass.
    with pytest.raises(RuntimeError):
        mdb = MoleculeDatabase(given_tc=-1)

    with pytest.raises(RuntimeError):
        mdb = MoleculeDatabase(given_tc=1.5)
