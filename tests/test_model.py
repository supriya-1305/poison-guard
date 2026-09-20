import torch

from ml.models.resnet18 import create_model


model = create_model(num_classes=10)

print("Model created successfully.")
print("Number of parameters:", sum(p.numel() for p in model.parameters()))

x = torch.randn(4, 3, 32, 32)

with torch.no_grad():
    output = model(x)

print("Input shape:", x.shape)
print("Output shape:", output.shape)

assert output.shape == (4, 10)

print("ResNet18 test PASSED.")
