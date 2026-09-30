
import subprocess
import sys
from pathlib import Path


LOG_FILE = Path(
    "experiments/week4/logs/activation_clustering.txt"
)


def main():
    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "ml.detection.activation_clustering"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    with LOG_FILE.open("w", encoding="utf-8") as log:
        for line in process.stdout:
            print(line, end="")
            log.write(line)
            log.flush()

    return_code = process.wait()

    print()
    print("Log saved to:")
    print(LOG_FILE)

    raise SystemExit(return_code)


if __name__ == "__main__":
    main()
