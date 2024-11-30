from pathlib import Path
from typing import Dict, List


class Settings:
    # Project structure
    PROJECT_ROOT = Path("characters")
    DATA_DIR = PROJECT_ROOT / "data"
    CONFIG_DIR = PROJECT_ROOT / "_config"
    TEMPLATES_DIR = CONFIG_DIR / "templates"

    # Character settings
    VALID_POSITIONS = ["WSP", "MB", "S", "L", "OPP"]
    VALID_RANKS = ["S", "A", "B", "C"]
    VALID_YEARS = [1, 2, 3]

    # Git settings
    GIT_ENABLED = True
    GIT_COMMIT_MESSAGE_TEMPLATE = "{operation}: {target}"

    @classmethod
    def initialize_directories(cls) -> None:
        """Initialize all required directories"""
        for dir_path in [cls.PROJECT_ROOT, cls.DATA_DIR, cls.CONFIG_DIR, cls.TEMPLATES_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)