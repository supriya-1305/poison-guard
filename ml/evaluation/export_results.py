import json
import pandas as pd


INPUT = (
    "experiments/week3/results/"
    "sanitization_results.json"
)

OUTPUT = (
    "experiments/week3/results/"
    "sanitization_results.csv"
)


def main():

    with open(INPUT, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    df.to_csv(
        OUTPUT,
        index=False
    )

    print("CSV created:")
    print(OUTPUT)

    print("\nRows:")
    print(len(df))

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()
