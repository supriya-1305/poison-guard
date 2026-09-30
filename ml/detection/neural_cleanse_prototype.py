import torch


def calculate_mask_anomaly(
    mask_norms
):

    values = torch.tensor(
        mask_norms,
        dtype=torch.float32
    )

    median = values.median()

    mad = torch.median(
        torch.abs(values - median)
    )

    if mad == 0:
        return torch.zeros_like(values)

    anomaly_index = (
        median - values
    ) / mad

    return anomaly_index


if __name__ == "__main__":

    example_norms = [
        10.0,
        9.5,
        11.0,
        10.2,
        2.1,
        10.5
    ]

    scores = calculate_mask_anomaly(
        example_norms
    )

    print("Neural Cleanse-style anomaly scores:")
    print(scores)
