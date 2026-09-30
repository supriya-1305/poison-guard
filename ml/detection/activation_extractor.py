import numpy as np
import torch
import torch.nn as nn
from torchvision.models import resnet18


class ActivationExtractor:

    def __init__(self, model_path):

        self.model = resnet18(weights=None)

        self.model.fc = nn.Linear(
            self.model.fc.in_features,
            10
        )

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location="cpu"
            )
        )

        self.model.eval()

        self.activations = None

        self.hook = (
            self.model.avgpool.register_forward_hook(
                self._hook
            )
        )

    def _hook(
        self,
        module,
        inputs,
        output
    ):

        self.activations = (
            output
            .detach()
            .cpu()
            .numpy()
        )

    def extract(self, images):

        tensor = torch.tensor(
            images,
            dtype=torch.float32
        )

        with torch.no_grad():

            self.model(tensor)

        features = self.activations

        features = features.reshape(
            features.shape[0],
            -1
        )

        return features

    def close(self):

        self.hook.remove()
