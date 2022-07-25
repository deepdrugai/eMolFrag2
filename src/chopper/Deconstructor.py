from rdkit import Chem
from eMolFrag2.src.utilities import constants
from eMolFrag2.src.utilities import logging
from eMolFrag2.src.chopper import BRICS_custom

def getMolMatrix(mol):
  """ 
  Molecule as Adjacency Matrix.

      Parameters: 
                mol (Rdkit.Mol): Molecule to get Matrix

      Returns: 
                m (matrix): Molecule Adjacency Matrix
  """
  return Chem.GetAdjacencyMatrix(mol)

def molAdjList(m):
  """ 
  Sorted Adjacency List

      Parameters:
                m (matrix): Molecule Adjacency Matrix

      Returns: 
                a (set of tuples): Adjacency List (sorted)
  """
  import numpy as np
  return {tuple(sorted(item)) for item in [*zip(*np.where(m==1))]} # adj_list as set

def molBRICSBonds(mol):
  """ 
  De-Duplicated BRICS Bonds List

      Parameters:
                mol (Rdkit.Mol): Molecule to get BRICS Bonds for

      Returns: 
                a (list of tuples): De-Duplicated BRICS Bonds List
  """
  snips = [(a, b) for (a, b), (c, d) in list(BRICS_custom.FindBRICSBonds(mol))]

  # reorder tuples as set
  return {(a, b) if (a < b) else (b, a) for a, b in snips}

def molFragments(l):
  """ 
  De-Duplicated BRICS Bonds List

      Parameters:
                l (matrix): Molecule Adjacency List

      Returns: 
                a (list of sets): List of Fragment Atom IDs as sets
  """
  import networkx as nx
  g = nx.from_edgelist(l)
  return list(nx.connected_components(g))

def combineAdjLinkerSequences(linkers, snips):
    """ 
        Sequences of adjacent linkers must be combined together to form
        a single linker.

        Parameters:
                linkers (set of tuples): atom ids of constituent atoms in fragment
                snips (set): Set of BRIC snips

        Returns: 
                linkers (set of tuples): Set of linkers (joined)
                snips_r (set): Set of snips to remove (we used them in joining)
    """
    snips_r = set() # snips to remove

    for x, y in snips:
        lx = [l for l in linkers if x in l] # List of linkers with x
        ly = [l for l in linkers if y in l] # List of linkers with y

        if lx and ly:
            lx, ly = *lx, *ly

            logging.logger.debug(f"Join linkers: {[lx, ly]} on {(x,y)}.")

            linkers -= {lx, ly} # Remove linkers 
            linkers.add(lx + ly) # Add merged linker
            snips_r.add((x, y)) # Add snip to removelist

            logging.logger.debug(f"All Linkers: {linkers}")
            logging.logger.debug(f"snips_r: {snips_r}")

    return linkers, snips_r

def computeFragmentsAndSnips(nxfrags, snips):
    """ 
        Return Final Brick, Linker and Snips Index List

        Parameters:
                nxfrags (list of sets): List of Fragment Atom IDs as sets
                snips (set): Set of BRIC snips

        Returns: 
                bricks (set): Set of bricks
                linkers (set): Set of linkers (joined)
                snips (set): Set of snips (joined)
    """
    # Check Linker v Bricks
    linkers = set() # set of linkers
    bricks = set() # set of bricks
  
    # split linkers & bricks (populate sets)
    [linkers.add(tuple(x)) if len(x) <= constants.LINKER_MAXIMUM_NUM_ATOMS else bricks.add(tuple(x)) for x in nxfrags]
    logging.logger.debug(f"(Before) All Bricks: {bricks}")
    logging.logger.debug(f"(Before) All Linkers: {linkers}")
    logging.logger.debug(f"(Before) Snips: {snips}")

    # Handle sequences of linkers
    linkers, snips_r = combineAdjLinkerSequences(linkers, snips)

    logging.logger.debug(f"(After) All Linkers: {linkers}")

    # Remove snip removelist from snip list
    snips -= snips_r
    
    logging.logger.debug(f"Final Snips: {snips}")

    return bricks, linkers, snips
    
def deconstruct(rdkit_mol):
    """
        Main deconstruction of an rdkit molecule into brickers, linkers and the
        BRICS cleave bonds between the fragments
        
        @input: molecule (Rdkit.Mol)
        @output: set of 
                bricks (set): Set of bricks (as tuples of integers)
                linkers (set): Set of linkers (joined) (as tuples of integers)
                snips (set): Set of snips (joined) (set of 2-tuples)
    """

    # Acquire an adjacency list of the graph corresponding to the input molecule
    adj_list = molAdjList(getMolMatrix(rdkit_mol))

    # Determine where BRICS intends to chop (minus L7 bonds due to BRICS_custom)
    snips = molBRICSBonds(rdkit_mol)

    # NetworkX-based fragment identification over the molecule minus
    # the BRICS snip points; fragments are connected components in the graph
    nxfrags = molFragments(adj_list - snips)

    # logger.setLevel("WARN")
    #logger.setLevel("DEBUG")

    return computeFragmentsAndSnips(nxfrags, snips)