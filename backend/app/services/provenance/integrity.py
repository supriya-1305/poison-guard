import hashlib
from pathlib import Path


def calculate_sha256(file_path: str | Path) -> str:
    """Calculate a file's SHA-256 digest without loading it all into memory."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def verify_sha256(file_path: str | Path, expected_sha256: str) -> dict:
    """Compare a file against a previously trusted SHA-256 digest."""

    if (
        len(expected_sha256) != 64
        or any(char not in "0123456789abcdefABCDEF"
               for char in expected_sha256)
    ):
        raise ValueError("Expected SHA-256 must contain 64 hexadecimal characters")

    actual = calculate_sha256(file_path)
    matches = actual.lower() == expected_sha256.lower()

    return {
        "file": str(Path(file_path)),
        "expected_sha256": expected_sha256.lower(),
        "actual_sha256": actual,
        "integrity_status": "VERIFIED" if matches else "MODIFIED",
        "revalidation_required": not matches,
    }
