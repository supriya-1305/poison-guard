from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


images = np.load("data/backdoor/images.npy")
metadata = __import__("json").load(
    open("data/backdoor/metadata.json")
)

poison_index = next(
    i for i, item in enumerate(metadata)
    if item["is_backdoor"]
)

clean_index = next(
    i for i, item in enumerate(metadata)
    if not item["is_backdoor"]
)

fig, axes = plt.subplots(1, 2, figsize=(6, 3))

axes[0].imshow(
    np.transpose(images[clean_index], (1, 2, 0))
)
axes[0].set_title("Clean")
axes[0].axis("off")

axes[1].imshow(
    np.transpose(images[poison_index], (1, 2, 0))
)
axes[1].set_title("Backdoored")
axes[1].axis("off")

Path("experiments/week4/figures").mkdir(
    parents=True,
    exist_ok=True
)

plt.tight_layout()

plt.savefig(
    "experiments/week4/figures/backdoor_trigger_example.png",
    dpi=200
)

plt.close()
