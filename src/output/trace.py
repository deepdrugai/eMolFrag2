# %%
from eMolFrag2.src.utilities.logging import log
from eMolFrag2.src.output import networktext as nt
import networkx as nx
from rdkit import Chem
import matplotlib.pyplot as plt


def mol_to_nx(mol):
    """Convert RDKit Object to NetworkX Object (Graph)

    Args:
        mol (_type_): RDKit Molecule

    Returns:
        G: NetorkX Graph
    """
    G = nx.Graph()

    for atom in mol.GetAtoms():
        G.add_node(atom.GetIdx(), atomic_num=atom.GetAtomicNum(), is_aromatic=atom.GetIsAromatic(), atom_symbol=atom.GetSymbol())

    for bond in mol.GetBonds():
        G.add_edge(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond_type=bond.GetBondType())

    return G


def example():
    # convert smiles string into a molecule EXAMPLE WITH CAFFEINE MOL
    mol_smile = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    mol = Chem.MolFromSmiles(mol_smile)

    # generate network text
    mol_nx = mol_to_nx(mol)
    nt.write_network_text(mol_nx, with_labels="atom_symbol")

    # print visual for comparison
    atoms = nx.get_node_attributes(mol_nx, "atom_symbol")
    color_map = {"C": "cyan", "O": "orange", "N": "magenta"}

    atom_colors = []
    for idx in mol_nx.nodes():
        if mol_nx.nodes[idx]["atom_symbol"] in color_map:
            atom_colors.append(color_map[mol_nx.nodes[idx]["atom_symbol"]])
        else:
            atom_colors.append("gray")

    nx.draw(mol_nx, labels=atoms, with_labels=True, node_color=atom_colors, node_size=800)
    plt.show()


def create_trace(mol):
    print("trace")
