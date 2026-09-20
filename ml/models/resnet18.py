import torch.nn as nn
from torchvision.models import resnet18


def create_model(num_classes=10):
    model = resnet18(weights=None)

    # CIFAR-10 uses 32x32 images.
    # Replace the original ImageNet-style first layer.
    model.conv1 = nn.Conv2d(
        3,
        64,
        kernel_size=3,
        stride=1,
        padding=1,
        bias=False
    )

    # Remove ImageNet max pooling.
    model.maxpool = nn.Identity()

    # Change final layer from 1000 classes to 10.
    model.fc = nn.Linear(
        model.fc.in_features,
        num_classes
    )

    return model
