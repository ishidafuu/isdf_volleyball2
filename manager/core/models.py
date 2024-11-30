from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Character:
    id: str
    name: Dict[str, str]
    position: str
    year: int
    height: int
    abilities: Dict[str, str]
    version: str
    last_updated: datetime

    @classmethod
    def validate(cls, data: Dict) -> bool:
        """Validate character data"""
        from character_manager.config.settings import Settings

        try:
            assert data["position"] in Settings.VALID_POSITIONS
            assert data["year"] in Settings.VALID_YEARS
            for ability in data["abilities"].values():
                assert ability in Settings.VALID_RANKS
            return True
        except (AssertionError, KeyError):
            return False