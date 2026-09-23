import torch

from ml.data.dataset import get_dataloaders
from ml.models.resnet18 import create_model
from ml.detection.feature_extractor import extract_features


def test_feature_extraction():

    print("\nLoading CIFAR-10...")

    _, _, test_loader = get_dataloaders()

    print("Loading trained ResNet18...")

    model = create_model()

    model.load_state_dict(
        torch.load(
            "models/resnet18_baseline.pth",
            map_location="cpu"
        )
    )

    print("Extracting features...")

    features, labels = extract_features(
        model,
        test_loader
    )

    print("Feature shape:", features.shape)
    print("Label shape:", labels.shape)

    assert features.shape[0] == 10000
    assert features.shape[1] == 512
    assert labels.shape[0] == 10000

    print("Feature extraction test PASSED.")
