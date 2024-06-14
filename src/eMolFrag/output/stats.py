import math

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from eMolFrag.utilities.logging import log


def histogram(dbs, out_dir):
    db_names = ["bricks", "linkers", "freeatoms"]

    for db, db_name in zip(dbs, db_names):
        if not hasattr(db, "database"):
            log.error(f"The database object for {db_name} does not have a 'database' attribute.")
            continue

        fragments_dict = {str(key).split(".sdf")[0]: len(value) + 1 for key, value in db.database.items()}

        log.debug(f"{db_name} count: {fragments_dict}")

        if not fragments_dict:
            log.info(f"No data to plot for {db_name}. Skipping...")
            continue

        # Preparing data for plotting
        sorted_items = sorted(fragments_dict.items(), key=lambda x: x[1], reverse=True)
        labels, values = zip(*sorted_items)
        widths = 0.8

        # Set up plot
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, width=widths)

        # Embed images into the bars if possible
        for i, label in enumerate(labels):
            image_path = out_dir / f"{label}.png"
            if image_path.exists():
                try:
                    img = mpimg.imread(image_path)
                    plt.imshow(img, extent=[i - widths / 2, i + widths / 2, values[i], values[i] + 1], aspect="auto", zorder=2)
                except Exception as e:
                    log.error(f"Failed to load image for {label}: {e}")

        plt.xlim(-0.5, len(labels) - 0.5)
        plt.ylim(0, max(values) + 1)
        plt.xticks([])
        plt.yticks(range(math.floor(min(values)), math.ceil(max(values)) + 1))
        plt.title(f"Histogram of {db_name.capitalize()} Fragment Frequency")
        plt.tight_layout()

        # Save the figure
        plt.savefig(out_dir / f"_hist_{db_name}_frags.png", dpi=300)
        plt.close()
        log.info(f"Histogram for {db_name} saved successfully.")
