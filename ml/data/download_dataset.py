from pathlib import Path
from torchvision import datasets


DATA_DIR = Path("data/raw")

DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading CIFAR-10...")
print(f"Dataset directory: {DATA_DIR.resolve()}")

train_dataset = datasets.CIFAR10(
    root=DATA_DIR,
    train=True,
    download=True
)

test_dataset = datasets.CIFAR10(
    root=DATA_DIR,
    train=False,
    download=True
)

print()
print("Dataset downloaded successfully.")
print("Training samples:", len(train_dataset))
print("Test samples:", len(test_dataset))
print("Number of classes:", len(train_dataset.classes))
print("Classes:", train_dataset.classes)
