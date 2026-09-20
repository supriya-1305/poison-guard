import time
import torch
import torch.nn as nn
import torch.optim as optim

import mlflow
import mlflow.pytorch

from ml.data.dataset import get_dataloaders
from ml.models.resnet18 import create_model


BATCH_SIZE = 128
EPOCHS = 10
LEARNING_RATE = 0.001


def get_device():

    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def evaluate(model, loader, criterion, device):

    model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)

            _, predicted = outputs.max(1)

            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    loss = total_loss / total
    accuracy = correct / total

    return loss, accuracy


def main():

    # --------------------------------------------------
    # 1. Select device
    # --------------------------------------------------

    device = get_device()

    print("Device:", device)

    # --------------------------------------------------
    # 2. Load CIFAR-10 DataLoaders
    # --------------------------------------------------

    print("Loading CIFAR-10 dataset...")

    train_loader, val_loader, test_loader = get_dataloaders()

    print("Training batches:", len(train_loader))
    print("Validation batches:", len(val_loader))
    print("Test batches:", len(test_loader))

    # --------------------------------------------------
    # 3. Create ResNet18 model
    # --------------------------------------------------

    model = create_model().to(device)

    # --------------------------------------------------
    # 4. Loss function
    # --------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    # --------------------------------------------------
    # 5. Optimizer
    # --------------------------------------------------

    optimizer = optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE
    )

    # --------------------------------------------------
    # 6. MLflow experiment
    # --------------------------------------------------

    mlflow.set_experiment("PoisonGuard-Baseline")

    # --------------------------------------------------
    # 7. Start MLflow run
    # --------------------------------------------------

    with mlflow.start_run():

        mlflow.log_param("model", "ResNet18")
        mlflow.log_param("dataset", "CIFAR-10")
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("learning_rate", LEARNING_RATE)
        mlflow.log_param("device", str(device))

        # --------------------------------------------------
        # 8. Start training timer
        # --------------------------------------------------

        start_time = time.time()

        # --------------------------------------------------
        # 9. Training loop
        # --------------------------------------------------

        for epoch in range(EPOCHS):

            model.train()

            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in train_loader:

                images = images.to(device)
                labels = labels.to(device)

                # Clear previous gradients
                optimizer.zero_grad()

                # Forward pass
                outputs = model(images)

                # Calculate loss
                loss = criterion(outputs, labels)

                # Backpropagation
                loss.backward()

                # Update weights
                optimizer.step()

                # Statistics
                running_loss += loss.item() * images.size(0)

                _, predicted = outputs.max(1)

                total += labels.size(0)

                correct += predicted.eq(labels).sum().item()

            # --------------------------------------------------
            # 10. Training metrics
            # --------------------------------------------------

            train_loss = running_loss / total
            train_accuracy = correct / total

            # --------------------------------------------------
            # 11. Validation
            # --------------------------------------------------

            val_loss, val_accuracy = evaluate(
                model,
                val_loader,
                criterion,
                device
            )

            # --------------------------------------------------
            # 12. Print epoch results
            # --------------------------------------------------

            print(
                f"Epoch {epoch + 1}/{EPOCHS} "
                f"Train Loss: {train_loss:.4f} "
                f"Train Acc: {train_accuracy:.4f} "
                f"Val Loss: {val_loss:.4f} "
                f"Val Acc: {val_accuracy:.4f}"
            )

            # --------------------------------------------------
            # 13. Log epoch metrics to MLflow
            # --------------------------------------------------

            mlflow.log_metric(
                "train_loss",
                train_loss,
                step=epoch
            )

            mlflow.log_metric(
                "train_accuracy",
                train_accuracy,
                step=epoch
            )

            mlflow.log_metric(
                "val_loss",
                val_loss,
                step=epoch
            )

            mlflow.log_metric(
                "val_accuracy",
                val_accuracy,
                step=epoch
            )

        # --------------------------------------------------
        # 14. Calculate training time
        # --------------------------------------------------

        training_time = time.time() - start_time

        # --------------------------------------------------
        # 15. Test the final clean model
        # --------------------------------------------------

        test_loss, test_accuracy = evaluate(
            model,
            test_loader,
            criterion,
            device
        )

        # --------------------------------------------------
        # 16. Log final test metrics
        # --------------------------------------------------

        mlflow.log_metric(
            "test_loss",
            test_loss
        )

        mlflow.log_metric(
            "test_accuracy",
            test_accuracy
        )

        mlflow.log_metric(
            "training_time_seconds",
            training_time
        )

        # --------------------------------------------------
        # 17. Print final results
        # --------------------------------------------------

        print()
        print("Final Results")
        print("----------------------")
        print("Test Loss:", test_loss)
        print("Test Accuracy:", test_accuracy)
        print("Training Time:", training_time, "seconds")

        # --------------------------------------------------
        # 18. Save PyTorch model FIRST
        # --------------------------------------------------

        torch.save(
            model.state_dict(),
            "models/resnet18_baseline.pth"
        )

        print()
        print("Model saved to:")
        print("models/resnet18_baseline.pth")

        # --------------------------------------------------
        # 19. MLflow model logging
        # --------------------------------------------------
        # MLflow 3.x requires an input example when using
        # the newer PyTorch serialization/tracing behavior.


        mlflow.pytorch.log_model(
            model,
            name="resnet18_baseline",
            serialization_format="pickle"
        )

        print("Model logged to MLflow successfully.")


if __name__ == "__main__":
    main()
