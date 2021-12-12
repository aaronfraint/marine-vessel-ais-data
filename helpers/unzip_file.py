import zipfile
from pathlib import Path


def extract_zipfile(filepath: Path) -> Path:
    """
    Extract a single .zip file to its parent folder.
    Return a filepath to the extracted CSV
    """

    message = f"Extracting {filepath.stem}"
    print(message)
    print("-" * len(message))

    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(filepath.parent)

    return Path(str(filepath).replace(".zip", ".csv"))
