from pathlib import Path
import sys


def contents_path(path: Path | str = "") -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve().joinpath(path)
    else:
        return Path(".").resolve().joinpath(path)
