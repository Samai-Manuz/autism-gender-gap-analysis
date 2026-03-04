from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "1_raw"
INTERIM_DIR = DATA_DIR / "2_interim"
PROCESSED_DIR = DATA_DIR / "3_processed"


@dataclass(frozen=True)
class Paths:
    project_root: Path = PROJECT_ROOT
    data_dir: Path = DATA_DIR
    raw_dir: Path = RAW_DIR
    interim_dir: Path = INTERIM_DIR
    processed_dir: Path = PROCESSED_DIR


def ensure_data_dirs() -> None:
    """Create expected data directories if they do not exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)