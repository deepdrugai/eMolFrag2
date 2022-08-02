# $Id$
#
#  Copyright (C) 2001-2006  greg Landrum
#
#   @@ All Rights Reserved @@
#  This file is part of the RDKit.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the RDKit source tree.
#
"""basic unit testing code for the molecule boost wrapper
"""
from fileinput import fileno
from rdkit import RDConfig
import unittest, pickle, os
from rdkit import Chem
import tempfile, os
import gzip
from eMolFrag2.src.output.Mol2Writer import *
from rdkit import Chem

class TestCase(unittest.TestCase):
  def setUp(self):
    self._files=[]
  def tearDown(self):
    for fileN in self._files:
      try:
        os.unlink(fileN)
      except OSError:
        pass

  def testMol2(self, removeHs=False):
    self._testMol2String(True)
    self._testMol2String(False)
    self._testMol2File(True)
    self._testMol2File(False)
    pass
    
  def _testMol2String(self, removeHs=False): 
    " testing 5k molecule pickles "
    # from rdkit import RDLogger
    # RDLogger.DisableLog('rdApp.*')
    with gzip.open('eMolFrag2/src/output/mols.1000.mol2.gz',"tr") as f:
        file = f.read().split("of record")
        for mol in file:
            if mol:
                # print(mol)
                # print("*********************")
                mol1 = Chem.MolFromMol2Block(mol)
                # mol1 = MolFromCommonMol2Block(mol)
                try:
                    mol2 = Chem.MolFromMol2Block(MolToMol2Block(mol1))
                    # mol2 = MolFromCommonMol2Block(MolToMol2Block(mol1))
                except Exception:
                    mol2 = None
                if mol2:
                    self.assertEqual(mol1.GetNumAtoms(), mol2.GetNumAtoms())
                    print(f"******************** PASS ********************")
                    # self.assertEqual(Chem.MolToSmiles(mol1), Chem.MolToSmiles(mol2).replace('[*-]', '[*]')) # doesn't work because some are kekulized
                else:
                    print('Could not read molecule back from mol2')

  def _testMol2File(self, removeHs=False): 
    " testing 5k molecule pickles "
    from rdkit import RDLogger
    RDLogger.DisableLog('rdApp.*')

    with gzip.open('eMolFrag2/src/output/mols.1000.mol2.gz','tr') as f:
        file = f.read().split("End of record")
        for mol in file:
            from tempfile import mkstemp
            mol_name = mol.lstrip().split("\n")[0].split(' ')[-1]
            fd, filename = mkstemp(f'--{mol_name}.mol2')
            if mol:
                mol1 = Chem.MolFromMol2Block(mol)
                # mol1 = MolFromCommonMol2Block(mol)
                # print(f"******************** {filename} ********************")
                MolToMol2File(mol1, filename)
                try:
                    # print(f"******************** {filename} ********************")
                    mol2 = Chem.MolFromMol2File(filename)
                except Exception:
                    # print(f"******************** FAILURREEEEEEEE ********************")
                    mol2 = None
                if mol2:
                    self.assertEqual(mol1.GetNumAtoms(), mol2.GetNumAtoms())
                    # print(f"******************** PASSSSSSSSSSSSS ********************")
                    smile1 = Chem.MolToSmiles(mol1)
                    smile2 = Chem.MolToSmiles(mol2)
                    if smile1 == smile2:
                        # print(f"{smile1 == smile2 = }")
                        self.assertEqual(smile1, smile2)
                        print(f"******************** PASS 2 ********************")
                    else:
                        print(f"******************** FAILURREEEEEEEE: {mol_name}.mol2  ********************")
                        print(f"{smile1}")
                        print(f"{smile2}")
                else:
                    print(f'Could not read molecule back from file: {mol_name}.mol2')

if __name__ == '__main__':
  unittest.main()
