from pathlib import Path
import pytest
from eMolFrag2.src.utilities import tc
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.representation.Molecule import Molecule


def four_mols():
    ms = ["uniqueMol(SMI)/DB01208.smi",
          "uniqueMol(SMI)/DB04626.smi",
          "uniqueMol(SMI)/DB11774.smi",
          "uniqueMol(SMI)/DB13499.smi"]
    mols = []
    for m in ms:
        mols.append(Molecule.to_mol(Path(__file__).parent / "data" / m))
    return mols


@pytest.mark.parametrize("mol1_path, mol2_path, expected", [
    (["similarPairSMI/1/DB00452.smi",
        "similarPairSMI/2/DB01137.smi",
        "similarPairSMI/3/DB12447.smi"],
        ["similarPairSMI/1/DB01421.smi",
            "similarPairSMI/2/DB01165.smi",
            "similarPairSMI/3/DB16219.smi"],
        [True, True, True]),
    (["uniqueMol(SMI)/DB00415.smi",
        "uniqueMol(SMI)/DB00415.smi",
        "uniqueMol(SMI)/DB01208.smi"],
     ["uniqueMol(SMI)/DB01208.smi",
        "uniqueMol(SMI)/DB04626.smi",
        "uniqueMol(SMI)/DB04626.smi"],
        [False, False, False],
     ),
    (["uniqueMol(SMI)/DB01208.smi",
        "uniqueMol(SMI)/DB04626.smi",
        "uniqueMol(SMI)/DB11774.smi",
        "uniqueMol(SMI)/DB13499.smi"],
        ["uniqueMol(SMI)/DB00415.smi"]*4,
        [False]*4)
])
def test_tc_equiv(mol1_path, mol2_path, expected):
    """
    Test to check the TC value given two molecules
    mol1_path : string Molecule1 Path
    mol2_path: string Molecule2 Path
    expected: bool Expected Boolean
    """
    cwd = Path(__file__).parent / "data"

    for m1, m2, r in zip(mol1_path, mol2_path, expected):
        log.debug(f"Input: {cwd / m1}\t{m2} \nassert = {r}")
        mol_obj1 = Molecule.to_mol(cwd / m1)
        mol_obj2 = Molecule.to_mol(cwd / m2)
        assert tc.TCEquiv(mol_obj1.getRDKitObject(),
                          mol_obj2.getRDKitObject()) == r
