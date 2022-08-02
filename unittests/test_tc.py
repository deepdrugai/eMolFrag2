from pathlib import Path
import pytest
from eMolFrag2.src.utilities import tc
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.representation.Molecule import Molecule
from eMolFrag2.src.input.MoleculeReader import getRDKitMolecule, to_mol

rel_path = "data"
@pytest.mark.parametrize("mol1_path, mol2_path, expected", (
        # Pair of molecules (.smi) with tc = 1.0
       (["similarPairSMI/1/DB00452.smi", "similarPairSMI/2/DB01137.smi", "similarPairSMI/3/DB12447.smi"],
        ["similarPairSMI/1/DB01421.smi", "similarPairSMI/2/DB01165.smi", "similarPairSMI/3/DB16219.smi"],
        [1.0] * 3),
))  # fmt: skip
def test_tc_private(mol1_path, mol2_path, expected):
    """
    Test tanimoto coefficient calculation from two rdkit molecules
    mol1_path string Molecule1 path
    mol2_path string Molecule2 path
    expected float expected tanimoto coefficient
    """
    cwd = Path(__file__).parent / rel_path

    for m1, m2, e in zip(mol1_path, mol2_path, expected):
        rdkit_mol1 = getRDKitMolecule(cwd / m1)
        rdkit_mol2 = getRDKitMolecule(cwd / m2)
        tanimoto = tc.TC(rdkit_mol1, rdkit_mol2)
        log.debug(f"Input: {m1}\t{m2}\t Expected vs Actual = {e} | {tanimoto}")
        # log.debug(f'TC Similiarity of {m1} and {m2}: {tanimoto}.')
        assert tanimoto == e


@pytest.fixture
def mols(tc_mols_list):
    mols = []
    for m in tc_mols_list:
        mols.append(to_mol(m))
    return mols


@pytest.fixture
def rdkit_mols(tc_mols_list):
    rdkit_list = []
    for m in tc_mols_list:
        rdkit_list.append(getRDKitMolecule(m))
    return rdkit_list


@pytest.fixture
def tc_mols_list():
    global rel_path
    ms = ["uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi", "uniqueMol(SMI)/DB04626.smi"]
    mols_list = []
    for m in ms:
        mols_list.append(Path(__file__).parent / rel_path / m)
    return mols_list


def tc_eval(mol1, mol2, expected_result):
    # log.debug(f"Input: \t{mol1}\t{mol2} \nexpected = {expected_result}")
    tc_diff = abs(tc.TC(mol1, mol2) - expected_result)
    log.debug(f"Distance from Expected TC: {tc_diff:.4f}")
    assert tc_diff <= 0.001


def test_tc(rdkit_mols, mols):
    """
    Test if two molecules match types and calculate tc vale
    rdkit_mols list List of RDKIT molecules
    mols list List of Local molecules
    """
    # Test different molecule type (1 rdkit molecule, 1 local molecule)
    tc_eval(rdkit_mols[0], mols[1], -1)
    tc_eval(mols[0], rdkit_mols[1], -1)

    # Test 2: two rdkit molecules
    tc_eval(rdkit_mols[0], rdkit_mols[1], 0.444)
    tc_eval(rdkit_mols[0], rdkit_mols[2], 0.293)
    tc_eval(rdkit_mols[1], rdkit_mols[2], 0.311)

    # Test 3: two local molecules
    tc_eval(mols[0], mols[1], 0.444)
    tc_eval(mols[0], mols[2], 0.293)
    tc_eval(mols[1], mols[2], 0.311)


@ pytest.mark.parametrize("mol1_path, mol2_path, expected", [
    (["similarPairSMI/1/DB00452.smi", "similarPairSMI/2/DB01137.smi", "similarPairSMI/3/DB12447.smi"],
     ["similarPairSMI/1/DB01421.smi", "similarPairSMI/2/DB01165.smi", "similarPairSMI/3/DB16219.smi"],
     [True] * 3),
    (["uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi"],
     ["uniqueMol(SMI)/DB01208.smi", "uniqueMol(SMI)/DB04626.smi", "uniqueMol(SMI)/DB04626.smi"],
     [False] * 3,
     ),
    (["uniqueMol(SMI)/DB01208.smi", "uniqueMol(SMI)/DB04626.smi", "uniqueMol(SMI)/DB11774.smi", "uniqueMol(SMI)/DB13499.smi"],
     ["uniqueMol(SMI)/DB00415.smi"] * 4,
     [False] * 4)
])  # fmt: skip
def test_tc_equiv(mol1_path, mol2_path, expected):
    """
    Test to check the TC value given two molecules
    mol1_path : string Molecule1 Path
    mol2_path: string Molecule2 Path
    expected: bool Expected Boolean
    """
    global rel_path
    cwd = Path(__file__).parent / rel_path

    for m1, m2, r in zip(mol1_path, mol2_path, expected):
        log.debug(f"Compare TC: {m1}\t{m2}\t Expected Equivalence = {r}")
        mol_obj1 = to_mol(cwd / m1)
        mol_obj2 = to_mol(cwd / m2)
        assert tc.TCEquiv(mol_obj1, mol_obj2) == r
