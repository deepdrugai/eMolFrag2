from eMolFrag2.src.utilities.logging import log
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math


def histogram(brick_db, linker_db, out_dir):
    dbs = [brick_db, linker_db]
    db_names = ["brick_bd", "linker_db"]
    for db, db_name in zip(dbs, db_names):
        # key = frags in database, value = num of mols in frag's value list (I'm not sure what they represent)
        mols = []
        width = 0.8
        new_dict = {}
        for key, value in db.database.items():
            if len(value) > 0:
                mols.append(out_dir / (str(key)[: str(key).index(".sdf")] + ".png"))
                new_dict[str(key)[: str(key).index(".sdf")]] = len(value)
        mols = list(set(mols))
        sorted_order = np.argsort(list(new_dict.values()))
        mols_sorted = list(np.array(mols)[sorted_order])
        dict_sorted = {key: value for key, value in sorted(new_dict.items(), key=lambda item: item[1], reverse=True)}
        labels = dict_sorted.keys()
        values = dict_sorted.values()
        plt.bar(labels, values, width=width)
        for i, (label, value) in enumerate(zip(labels, values)):
            img = mpimg.imread(mols_sorted[i])
            plt.imshow(img, extent=[i - width / 2, i + width / 2, value, value + 1], aspect="auto", zorder=2)
        plt.xlim(-0.5, len(labels) + 1)
        plt.ylim(0, max(values) + 1)
        plt.xticks([])
        plt.yticks(range(math.floor(min(values)), math.ceil(max(values)) + 1))
        plt.title("Histogram of Fragment Frequency")
        plt.tight_layout()
        plt.savefig(out_dir / f"{db_name}_frags.png", dpi=300)
        plt.close()
