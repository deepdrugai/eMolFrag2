from eMolFrag.chopper import Connectivity, Deconstructor, Fragmenter, Preprocessor
from eMolFrag.representation import Brick, FreeAtom, Linker
from eMolFrag.representation import MoleculeDatabase as MDB
from eMolFrag.utilities import constants
from eMolFrag.utilities.logging import log


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
    bricks, linkers, snips, freeatoms = Deconstructor.deconstruct(mol)

    #
    # (5): Compute connectivity among free radicals
    #      This computation modifies the molecule with property information
    Connectivity.compute(mol, snips)

    #
    # (6): Perform the actual chop
    #
    return Fragmenter.fragmentAll(mol, bricks, linkers, freeatoms), snips


def chopall(mols):
    """
    Chop many molecules

    @input: list of Molecule objects (containing rdkit objects)

    @output: MoleculeDatabase of brick fragments
    @output: MoleculeDatabase of linker fragments
    """
    brick_db = MDB.MoleculeDatabase(constants.DEFAULT_TC_UNIQUENESS)
    linker_db = MDB.MoleculeDatabase(constants.DEFAULT_TC_LINKER_UNIQUENESS)
    fa_db = MDB.MoleculeDatabase(constants.DEFAULT_TC_LINKER_UNIQUENESS)
    snip_db = {}

    for mol in mols:
        log.info(f"Processing molecule {mol.getFileName()}.")

        #
        # Chop
        #
        (bricks, linkers, freeatoms), snips = chop(mol.getRDKitObject())

        #
        # Process the results
        #
        results = brick_db.addAll([Brick.Brick(b, mol, suffix=index) for index, b in enumerate(bricks)])

        log.info(f"Added {len(bricks)} brick{'s'[:len(bricks) ^ 1]};\t({len(results)} TC-Unique)")

        results = linker_db.addAll([Linker.Linker(ell, mol, suffix=index) for index, ell in enumerate(linkers)])

        log.info(f"Added {len(linkers)} linker{'s'[:len(linkers) ^ 1]};\t({len(results)} TC-Unique)")

        results = fa_db.addAll([FreeAtom.FreeAtom(fa, mol, suffix=index) for index, fa in enumerate(freeatoms)])

        log.info(f"Added {len(freeatoms)} freeatom{'s'[:len(freeatoms) ^ 1]};\t({len(results)} TC-Unique)")

        #
        # Handle snips and convert atom ids
        #
        og_map = {}
        for mdb in [brick_db, linker_db, fa_db]:
            for frag in mdb.GetAllMolecules():
                for a in frag.getRDKitObject().GetAtoms():
                    idx = a.GetIdx()
                    idx_og = a.GetIntProp("original_idx")

                    # Check if the id_og is in any of the snips
                    found = any(idx_og in snip for snip in snips)

                    # Iterate through each snip in snips and add mapping to og_map
                    if found:
                        og_map.update(
                            {idx_og: f"{frag.getFileName()}-{idx:03d} ({a.GetSymbol()} {idx_og})" for snip in snips if idx_og in snip}
                        )
                    # ruff: noqa: B035

        # Create a new set of snips with replaced/mapped keys
        snips_new = set()

        for snip in snips:
            temp_tuple = tuple(og_map[key] for key in snip if key in og_map)
            snips_new.add(temp_tuple)

        snip_db[mol.getFileName()] = snips_new

        log.info(f"Added {len(snips)} snip{'s'[:len(snips) ^ 1]}.")

    return brick_db, linker_db, fa_db, snip_db
