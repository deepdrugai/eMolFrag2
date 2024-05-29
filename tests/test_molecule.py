# import py
from pathlib import Path

import pytest
from eMolFrag.input.MoleculeReader import to_mol
from eMolFrag.utilities.logging import log

data = Path(__file__).parent.parent / "data"
ms = ["similarPairSMI/3/DB12447.smi", "uniqueMol(SMI)/DB00415.smi"]


@pytest.fixture
def file_names():
    file_name = []
    for m in ms:
        name = m.split("/")
        file_name.append(name[len(name) - 1])
    return file_name


@pytest.fixture
def mols():
    list_mols = []
    for m in ms:
        path = data / m
        list_mols.append(to_mol(path))
    return list_mols


def test_mol_file_parent_name(mols, file_names):
    """Testing the molecule object"""
    for m in mols:
        log.info(f"Parent name : {m.getParent()}; File Name: {m.getFileName()}")
        assert m.getParent() is None
        assert m.getFileName() in file_names


def test_clear_prop_to_sdf(mols):
    """Testing the clear properties"""
    for m in mols:
        log.info(f"RDKit Object: {m.getRDKitObject().GetPropNames()}")
        mol_to_sdf = m._toSDF()
        log.info(f"RDKit Object: {type(mol_to_sdf)}")
        mol_clear = m.clearProperties()
        assert mol_clear is None
        assert isinstance(mol_to_sdf, str)


@pytest.mark.parametrize(("mol_path1", "mol_path2", "expected"), [
    ("uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi", False),
    ("similarPairSMI/1/DB01421.smi", "similarPairSMI/1/DB01421.smi", True),
    ])  # fmt: skip
def test_eq_mols(mol_path1, mol_path2, expected):
    path1 = data / mol_path1
    path2 = data / mol_path2
    mol1 = to_mol(path1)
    mol2 = to_mol(path2)
    log.info(f"Molecule as String: {str(mol1) == str(mol2)}")
    assert (mol1 == mol2) == expected
    assert (str(mol1) == str(mol2)) == expected


def test_fragment_name(mols):
    """Test the Fragment Name"""
    for m in mols:
        frag_name = m.makeFragmentFileName(file_name=m.getFileName())
        log.info(f"Fragment Name: {frag_name}")
        assert frag_name.split("-")[1] == m.getFileName()
