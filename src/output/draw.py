from rdkit import Chem
from rdkit.Chem import BRICS, Draw
from rdkit.Chem.Draw import rdMolDraw2D

from eMolFrag2.src.chopper.Deconstructor import deconstruct
from eMolFrag2.src.utilities.logging import log

# from rdkit.Chem.Draw import IPythonConsole
# from rdkit.Chem import Draw
# from IPython.display import SVG
# FIXME pls fix SVG

# IPythonConsole.ipython_useSVG = True  #< set this to False if you want PNGs instead of SVGs
# IPythonConsole.molSize = 500,500  # Draw Original Molecule


def draw_mol(mol, out_dir):
    # log.debug(out_dir)
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    img = Chem.Draw.MolToImage(mol, imageType="png")
    img = img.save(out_dir)
    # with open(out_dir / 'test2.png','wb+') as outfile:
    #     outfile.write(img.data.encode('utf-8'))


def draw_grid_img(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    # IPythonConsole.drawOptions.addAtomIndices = True
    frags = BRICS.BRICSDecompose(mol, returnMols=True)
    img = Draw.MolsToGridImage(frags, molsPerRow=3, subImgSize=(250, 250))
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.data.encode("utf-8"))


def draw_grid_img2(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    single_mol_frags = BRICS.BreakBRICSBonds(mol)
    frags = Chem.GetMolFrags(single_mol_frags, asMols=True)
    img = Draw.MolsToGridImage(frags)
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.data.encode("utf-8"))


def highlight_cleave_sights(mol, out_dir):
    # mol = Chem.MolFromSmiles('[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[C@H](N)C1=CC=C(O)C=C1)C(O)=O')
    bricks, linkers, snips = deconstruct(mol)
    log.debug(bricks, linkers, snips)
    cleavesites = [x for xs in snips for x in xs]
    cp = Chem.Mol(mol)
    d2d = rdMolDraw2D.MolDraw2DSVG(600, 400)
    d2d.drawOptions().addAtomIndices = True
    d2d.drawOptions().addBondIndices = False
    # Test this line to make sure it properly highlights cleaved bonds?
    d2d.DrawMolecule(cp, highlightAtoms=cleavesites, highlightBonds=sorted(cleavesites)[::2])
    d2d.FinishDrawing()
    img = SVG(d2d.GetDrawingText())
    with open(out_dir, "wb+") as outfile:
        outfile.write(img.data.encode("utf-8"))
