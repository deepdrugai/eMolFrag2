# from cmath import exp
# from isort import file
import pytest
from pathlib import Path
# from rdkit import Chem
# from eMolFrag2.src.utilities import constants #, tc
# from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.chopper import Chopper
# from eMolFrag2.src.representation import MoleculeDatabase as MDB
# from eMolFrag2.src.representation import Brick
# from eMolFrag2.src.representation import Linker 
from eMolFrag2.src.input.MoleculeReader import to_mol

cwd = Path(__file__).parent / "data"

@pytest.fixture
def output():
  expectedLinks = [
    "l-CHEMBL9070.mol2-000.sdf"
    ]    
    
  expectedBricks = [
    "b-CHEMBL9070.mol2-000.sdf", 
    "b-CHEMBL9070.mol2-001.sdf", 
    "b-CHEMBL9070.mol2-002.sdf", 
    "b-CHEMBL9070.mol2-003.sdf", 
    "b-CHEMBL9070.mol2-004.sdf"
    ]
  return expectedBricks, expectedLinks

@pytest.mark.parametrize("input", [
  # Molecule
  ([to_mol(cwd / "db-files/mol2-b-l/input/CHEMBL9070.mol2")])
])
def test_chopall(input, output):
# get bricks and linkers from input 
    bricks, links = Chopper.chopall(input)
    eBrick, eLink = output
# compare if expected links are equal to actual links
    for line in links.GetAllMolecules():
      assert eLink.__contains__(line.toSDF()[0:25])
 
# compare if expected bricks are equal to actual bricks
    for line in bricks.GetAllMolecules():
      assert eBrick.__contains__(line.toSDF()[0:25]) 
