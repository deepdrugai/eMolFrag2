import pytest
from pathlib import Path
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.representation.Molecule import Molecule
from eMolFrag2.src.representation.MoleculeDatabase import MoleculeDatabase

# Moved to Molecule file
# def to_mol(molPath):
#   """ Create Molecule object from file path """
#   mol = utilities.getRDKitMolecule(molPath)
#   log.debug(f"{mol} {molPath}")
#   m = Molecule(mol, molPath.name)
#   log.debug(f"{m}")
#   return m

@pytest.fixture
def tc1_mol_pairs():
    ms = [("similarPairSMI/1/DB00452.smi",
          "similarPairSMI/1/DB01421.smi"),
          ("similarPairSMI/2/DB01137.smi",
          "similarPairSMI/2/DB01165.smi"),
          ("similarPairSMI/3/DB12447.smi",
          "similarPairSMI/3/DB16219.smi")]
    molpairs = []
    dir = Path(__file__).parent / "data"
    for a, b in ms:
        am = Molecule.to_mol(dir / a)
        bm = Molecule.to_mol(dir / b)
        molpairs.append([am, bm])
    return molpairs


@pytest.fixture
def five_mols():
    ms = ["uniqueMol(SMI)/DB00415.smi",
          "uniqueMol(SMI)/DB01208.smi",
          "uniqueMol(SMI)/DB04626.smi",
          "uniqueMol(SMI)/DB11774.smi",
          "uniqueMol(SMI)/DB13499.smi"]
    mols = []
    dir = Path(__file__).parent / "data"
    for m in ms:
        mols.append(Molecule.to_mol(dir / m))
    return mols


@pytest.mark.parametrize("input, expected", [
    # Single Molecules
    (["similarPairSMI/3/DB12447.smi"], [True]),
    (["similarPairSMI/3/DB16219.smi"], [True]),
    # Molecules with tc = 1.0
    (["similarPairSMI/3/DB12447.smi", "similarPairSMI/3/DB12447.smi"],
        [True, False]),  # Same molecule
    (["similarPairSMI/3/DB12447.smi", "similarPairSMI/3/DB16219.smi"],
        [True, False]),  # Two molecules of TC = 1.0
    # Five Molecules with tc < 1.0
    (["uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi",
      "uniqueMol(SMI)/DB04626.smi", "uniqueMol(SMI)/DB11774.smi",
      "uniqueMol(SMI)/DB13499.smi"], [True] * 5)
])
def test_add_mol_to_mdb(input, expected, tc=1.0):
    """ Test adding TC Equivalent molecules to Molecule Database where given_tc = 1"""

    dir = Path(__file__).parent / "data"
    mdb = MoleculeDatabase(given_tc=tc)

    for m, e in zip(input, expected):
        log.debug(f"{dir / m}\t{e}")
        assert mdb.add(Molecule.to_mol(dir / m)) is e


def test_add_list_to_mdb(five_mols, tc=1.0):
    """ Test adding a list to molecule database """
    mdb = MoleculeDatabase(tc)
    log.debug(f"{len(five_mols) = }")
    assert len(mdb.addAll(five_mols)) == len(five_mols)


def test_get_unique_molecules_mdb(five_mols, tc1_mol_pairs):
    """ Test adding a large number of mols to molecules database and get unique """

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
    """ Test adding a large number of mols to molecules database and get total molecules """

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
