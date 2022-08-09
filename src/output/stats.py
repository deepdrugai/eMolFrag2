from eMolFrag2.src.utilities.logging import log
import matplotlib.pyplot as plt
import seaborn as sns
import math
from eMolFrag2.src.output.draw import draw_mol
import matplotlib.image as mpimg


#order most to least common
def histogram(brick_db, linker_db, out_dir):
    dbs = [brick_db, linker_db]
    db_names = ['brick_bd', 'linker_db']
    for db, db_name in zip(dbs, db_names):
        #key = frags in database, value = num of mols in frag's value list (I'm not sure what they represent)
        mols = []
        width = 0.8
        for key, value in db.database.items():
            if len(value) > 0:
                draw_mol(key.getRDKitObject(), out_dir / (str(key)[:str(key).index('.')] + '.png'))
                mols.append(out_dir / (str(key)[:str(key).index('.')] + '.png'))
        mols = list(set(mols))
        dict = {str(key.getFileName()[:str(key).index('.')]): len(value) for key, value in db.database.items()}
        dict_filt = {key:value for key,value in dict.items() if value!=0}
        labels = dict_filt.keys()
        values = dict_filt.values()
        ax = plt.bar(labels, values, width = width)
        #plt.bar_label(ax, labels=labels, rotation=90, padding=10)
        for i, (label, value) in enumerate(zip(labels, values)):
            img = mpimg.imread(mols[i])
            plt.imshow(img, extent=[i - width / 2, i + width / 2,value, value+1], aspect='auto', zorder=2)
        plt.xlim(-0.5, len(labels)+1)
        plt.ylim(0, max(values)+1)
        plt.xticks([])
        plt.yticks(range(math.floor(min(values)), math.ceil(max(values))+1))
        plt.title('Hayden\'s Awesome Graph')
        sns.despine()
        plt.tight_layout()
        plt.savefig(out_dir / f'{db_name}_frags.png', dpi=300)
        plt.close()