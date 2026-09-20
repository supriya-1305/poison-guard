from ml.data.dataset import get_dataloaders


train_loader, val_loader, test_loader = get_dataloaders()

print("Train batches:", len(train_loader))
print("Validation batches:", len(val_loader))
print("Test batches:", len(test_loader))

images, labels = next(iter(train_loader))

print("Image shape:", images.shape)
print("Label shape:", labels.shape)
