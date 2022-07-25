from rdkit import Chem
from eMolFrag2.src.utilities import *
from eMolFrag2.src.chopper import Preprocessor
from eMolFrag2.src.chopper import Deconstructor
from eMolFrag2.src.chopper import Connectivity
from eMolFrag2.src.chopper import Fragmenter
from eMolFrag2.src.representation import MoleculeDatabase as MDB
from eMolFrag2.src.representation import Brick
from eMolFrag2.src.representation import Linker

def chop(rdkit_mol):
    """
        0. We work on a copy of the input molecule with hydrogens removed and
           atom type information within the molecule 

        Chopping consists of the following algorithm:
            1. Build graph of molecule
            2. Find where BRICS would cleave (BRICS bonds) [snips in the code]
                 * We modify FindBRICSBonds code to ensure that L7 bonds are never
                   cleaved (according eMolFrag v1.0)
                 * Modified in BRICS_custom.py
            3. Break graph into fragments
                 Take the graph of molecule, substract proposed BRICS bonds
                 The resulting molecule is a disconnected set of subgraphs.
                 Each of these subgraphs is a fragment.
                 Those fragments with fewer than 4 atoms are the first phase of
                 linkers; all others are bricks
            4. Combine sequences of Linker-Linker fragments into single a Linker

            5. Compute connectivity of free radicals (from each snip calc atomtype of tuple pairs)

            6. Break each fragment into Rdkit.Mol objectPerform actual break of chop
            
        Input: An rdkit molecule (ideally, with AtomType info from mol2 format)
            
        Output: list of Rdkit.Mol Bricks, list of Rdkit.Mol Linkers
    """
    # (0)
    mol = Preprocessor.preprocess(rdkit_mol)

    #
    # Steps (1) - (4)
    # Deconstruct our molecule into the known fragments
    # These are sets of atom indices (bricks, linkers); snips are a set of bonds.
    #    * All such information 'references' the molecule, but does not modify it
    #
    bricks, linkers, snips = Deconstructor.deconstruct(mol)

    #
    # (5): Compute connectivity among free radicals
    #      This computation modifies the molecule with property information
    Connectivity.compute(mol, snips)

    #
    # (6): Perform the actual chop
    #
    return Fragmenter.fragmentAll(mol, bricks, linkers)

def chopall(mols):
    """
        Chop many molecules
        
        @input: list of Molecule objects (containing rdkit objects)
        
        @output: MoleculeDatabase of brick fragments
        @output: MoleculeDatabase of linker fragments        
    """
    brick_db = MDB.MoleculeDatabase(constants.DEFAULT_TC_UNIQUENESS)
    linker_db = MDB.MoleculeDatabase(constants.DEFAULT_TC_LINKER_UNIQUENESS)

    for mol in mols:

        logging.logger.debug(f'Processing molecule{mol.getFileName()}')

        #
        # Chop
        #
        bricks, linkers = chop(mol.getRDKitObject())

        #
        # Process the results
        #
        results = brick_db.addAll([Brick.Brick(b, mol, suffix = index) for index, b in enumerate(bricks)])
    
        logging.logger.debug(f'Added {len(results)} TC-unique bricks; \
                             {len(bricks) - len(results)} were TC-redundant')

        results = linker_db.addAll([Linker.Linker(ell, mol, suffix = index) for index, ell in enumerate(linkers)])

        logging.logger.debug(f'Added {len(results)} TC-unique linkers; \
                             {len(linkers) - len(results)} were TC-redundant')

    return brick_db, linker_db