import torch
import torch.nn as nn


def get_device():

    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def create_feature_model(model):

    model.fc = nn.Identity()

    return model


def extract_features(model, dataloader):

    device = get_device()

    model = create_feature_model(model)

    model = model.to(device)

    model.eval()

    features = []
    labels = []

    with torch.no_grad():

        for images, batch_labels in dataloader:

            images = images.to(device)

            outputs = model(images)

            features.append(
                outputs.cpu()
            )

            labels.append(
                batch_labels
            )

    features = torch.cat(
        features
    ).numpy()

    labels = torch.cat(
        labels
    ).numpy()

    return features, labels
