import pytest
from pathlib import Path
from eMolFrag2.src.representation.Molecule import Molecule
from eMolFrag2.src.input.MoleculeReader import to_mol
from eMolFrag2.src.utilities.logging import log

dir = Path(__file__).parent / "data"

@pytest.mark.parametrize("mol_path", [("similarPairSMI/3/DB12447.smi"), ("uniqueMol(SMI)/DB00415.smi")])
def test_mol_file_parent_name(mol_path):
    """Testing the molecule object"""
    log.info(f"Molecule Path : {dir / mol_path}")
    path = dir / mol_path
    mol = to_mol(path)
    log.info(
        f"Parent name : {mol.getParent()}; File Name: {mol.getFileName()}")
    assert mol.getParent() is None and mol.getFileName() is not None


@pytest.mark.parametrize("mol_path", [("similarPairSMI/3/DB12447.smi"), ("uniqueMol(SMI)/DB00415.smi")])
def test_clear_prop_to_sdf(mol_path):
    """Testing the clear properties"""
    path = dir / mol_path
    mol = to_mol(path)
    log.info(f"RDKit Object: {mol.getRDKitObject().GetPropNames()}")
    mol_to_sdf = mol._toSDF()
    log.info(f"RDKit Object: {type(mol_to_sdf)}")
    mol_clear = mol.clearProperties()
    assert mol_clear is None and type(mol_to_sdf) is str


@pytest.mark.parametrize("mol_path1, mol_path2, expected", [("uniqueMol(SMI)/DB00415.smi", "uniqueMol(SMI)/DB01208.smi", False),
("similarPairSMI/1/DB01421.smi", "similarPairSMI/1/DB01421.smi", True)])
def test_eq_mols(mol_path1, mol_path2, expected):
    path1 = dir / mol_path1
    path2 = dir / mol_path2
    mol1 = to_mol(path1)
    mol2 = to_mol(path2)
    log.debug(f"Molecule as String: {str(mol1) == str(mol2)}")
    log.debug(f"String Molecule: {str(mol1)} and {str(mol2)}")
    assert (mol1 == mol2) == expected and (str(mol1) == str(mol2)) == expected
