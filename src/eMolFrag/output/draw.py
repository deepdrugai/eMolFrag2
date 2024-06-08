# %%
from rdkit import Chem
from rdkit.Chem import BRICS
from rdkit.Chem.Draw import MolsToGridImage, MolToFile

from eMolFrag.chopper.Chopper import chop
from eMolFrag.utilities.logging import log

# from IPython.display import SVG


def draw_mol(mol, out_dir, **kwargs):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    MolToFile(mol, out_dir, **kwargs)


def draw_grid_img(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    frags = BRICS.BRICSDecompose(mol, returnMols=True)
    img = MolsToGridImage(frags, molsPerRow=3, subImgSize=(250, 250), useSVG=True)
    log.debug(type(img))
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.encode("utf-8"))


def draw_grid_img2(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    mol.RemoveAllConformers()
    single_mol_frags = BRICS.BreakBRICSBonds(mol)
    frags = Chem.GetMolFrags(single_mol_frags, asMols=True)
    img = MolsToGridImage(frags, molsPerRow=3, subImgSize=(250, 250), useSVG=True)
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.encode("utf-8"))


# def highlight_cleave_sights(mol):
#     # mol.RemoveAllConformers()
#     _, snips = chop(mol)
#     snip_atoms = [x for xs in snips for x in xs]
#     log.debug(snip_atoms)
#     snip_bonds = []
#     for atom1, atom2 in snips:
#         snip_bonds.append(mol.GetBondBetweenAtoms(atom1, atom2).GetIdx())
#     log.debug(snip_bonds)

#     cp = Chem.Mol(mol)
#     d2d = rdMolDraw2D.MolDraw2DSVG(600, 400)
#     d2d.drawOptions().addAtomIndices = True
#     # d2d.drawOptions().addBondIndices = True
#     d2d.DrawMolecule(cp, highlightAtoms=snip_atoms, highlightBonds=snip_bonds)
#     d2d.FinishDrawing()
#     return SVG(d2d.GetDrawingText())
#     # img = d2d.GetDrawingText()
#     # with open(out_dir, "wb+") as outfile:
#     #     outfile.write(img.encode("utf-8"))


def highlight_cleave_sights2(mol):
    # mol.RemoveAllConformers()
    _, snips = chop(mol)
    snip_atoms = [x for xs in snips for x in xs]
    log.debug(snip_atoms)
    # snip_bonds = []
    # for atom1, atom2 in snips:
    #     snip_bonds.append(mol.GetBondBetweenAtoms(atom1, atom2).GetIdx())
    snip_bonds = [mol.GetBondBetweenAtoms(atom1, atom2).GetIdx() for atom1, atom2 in snips]

    MolToFile(mol, filename="/home/bess/dev/eMolFrag2/outputtest/magic5.svg", highlightBonds=snip_bonds)


# mol = Chem.MolFromSmiles("[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O")
# DB11537 is not reconstructing
# DB01190 is not reconstructing
mol = Chem.MolFromSmiles("[H][C@@](NC(=O)[C@@H]1C[C@H](CC)CCN1)([C@H](C)Cl)[C@@]1([H])O[C@H](SC)[C@H](O)[C@@H](O)[C@H]1O")
# C.3 N.Am
# highlight_cleave_sights2(mol)
