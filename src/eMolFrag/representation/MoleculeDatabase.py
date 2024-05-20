# from rdkit import DataStructs # For TC Computations

# import sys
from eMolFrag.utilities import constants
from eMolFrag.utilities import tc
from eMolFrag.utilities.logging import log

from eMolFrag.representation.Molecule import Molecule


#
# This class will simulate an equivalence class of molecules
#
#    We have a dictionary of the form <Molecule, [TC-'Equivalent' Molecules]>
#
class MoleculeDatabase(Molecule):
    def __init__(self, given_tc=constants.DEFAULT_TC_UNIQUENESS):
        self.database = {}

        if given_tc < 0 or given_tc > 1:
            log.error(f"Tanimoto coefficient constant {given_tc} is not in allowable range 0 <= tc <= 1.0")
            raise RuntimeError

        self.TC_THRESH = given_tc

    #
    # Add one Molecule object to the database
    #
    # @output: if the given molecule is unique, return True (False if it is TC-redudant)
    #
    def add(self, molecule):
        # print("Adding", molecule.getFileName())

        tc_equiv = [db_mol for db_mol in self.database.keys() if tc.TCEquiv(molecule, db_mol, tc_threshold=self.TC_THRESH)]

        if len(tc_equiv) > 1:
            log.debug(f"Internal MoleculeDatabase error; {len(tc_equiv)}-TC equivalent molecules")

        # Empty ; we have a unique fragment; a new entry has { molecule, [] }
        if not tc_equiv:
            self.database[molecule] = []
            return True

        # TC-similar fragment: { tc_equiv, [..., molecule] }
        # Add this molecule as being similar to all other molecules in this equivalence class
        tc_equiv[0].addTCSimilar(molecule)
        for sim_mol in self.database[tc_equiv[0]]:
            sim_mol.addTCSimilar(molecule)
        self.database[tc_equiv[0]].append(molecule)

        return False

    #
    # Add a list of molecules
    # @output: the list of UNIQUE database additions
    #          (redundant count can be computed by user)
    #
    def addAll(self, molecules):
        return [mol for mol in molecules if self.add(mol)]

    def GetUniqueMolecules(self):
        return list(self.database.keys())

    #
    # Return all Molecule objects stored
    #
    def GetAllMolecules(self):
        return [*self.database.keys()] + [mol for lst in self.database.values() for mol in lst]

    #
    # Return all TC>1 objects stored
    #
    def GetAllTCEqual(self):
        for mol, equivalent in self.database.items():
            log.error(equivalent)
            log.error(f'\n{mol.getFileName()}: [{", ".join([eq_mol.getFileName() for eq_mol in equivalent])}]')
        return [*self.database.keys()] + [mol for lst in self.database.values() for mol in lst]

    def numAllMolecules(self):
        return len(self.GetAllMolecules())

    def __len__(self):
        return len(self.database)

    def __str__(self):
        """
        Output of the equivalences classes represented in this database
        """
        string = ""
        for mol, equivalent in self.database.items():
            string += f'\n{mol.getFileName()}: [{", ".join([eq_mol.getFileName() for eq_mol in equivalent])}]'
        # for mol, equivalent in self.database.items():
        #     if equivalent:
        #         log.error(f"\n{mol.getFileName()}: {[eq_mol.getFileName() for eq_mol in equivalent]}")
        #         log.error(f'\n{mol.getFileName()}: [{", ".join([eq_mol.getFileName() for eq_mol in equivalent])}]')
        return string
