import zipfile
from pathlib import Path

from .timer import print_message_and_timer


@print_message_and_timer("Extracting CSV")
def extract_zipfile(filepath: Path) -> Path:
    """
    Extract a single .zip file to its parent folder.
    Return a filepath to the extracted CSV
    """

    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(filepath.parent)

    return Path(str(filepath).replace(".zip", ".csv"))
