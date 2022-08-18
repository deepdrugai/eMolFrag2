from rdkit import Chem
from rdkit.Chem import BRICS, Draw
from rdkit.Chem.Draw import rdMolDraw2D

from eMolFrag2.src.chopper.Deconstructor import deconstruct
from eMolFrag2.src.utilities.logging import log

def draw_mol(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    Chem.Draw.MolToFile(mol, out_dir)


def draw_grid_img(mol, out_dir):
    #mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    frags = BRICS.BRICSDecompose(mol, returnMols=True)
    img = Draw.MolsToGridImage(frags, molsPerRow=3, subImgSize=(250, 250), useSVG=True)
    log.debug(type(img))
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.encode("utf-8"))


def draw_grid_img2(mol, out_dir):
    #mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    single_mol_frags = BRICS.BreakBRICSBonds(mol)
    frags = Chem.GetMolFrags(single_mol_frags, asMols=True)
    img = Draw.MolsToGridImage(frags, molsPerRow=3, subImgSize=(250, 250), useSVG=True)
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.encode("utf-8"))


def highlight_cleave_sights(mol, out_dir):
    #mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    bricks, linkers, snips = deconstruct(mol)
    cleavesites = [x for xs in snips for x in xs]
    bond_indices = []
    for snip in snips:
        atom1, atom2 = snip
        bond = mol.GetBondBetweenAtoms(atom1, atom2)
        bond_indice = bond.GetIdx()
        bond_indices.append(bond_indice)
    cp = Chem.Mol(mol)
    d2d = rdMolDraw2D.MolDraw2DSVG(600, 400)
    d2d.drawOptions().addAtomIndices = True
    d2d.drawOptions().addBondIndices = False
    d2d.DrawMolecule(cp, highlightAtoms=cleavesites, highlightBonds=bond_indices)
    log.debug(cleavesites)
    d2d.FinishDrawing()
    img = d2d.GetDrawingText()   
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.encode("utf-8"))
