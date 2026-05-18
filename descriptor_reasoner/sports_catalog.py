from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SportConfig:
    key: str
    display_name: str
    max_score: float
    descriptor_focus: List[str]
    criteria_weights: Optional[Dict[str, float]] = None


class SportsCatalog:
    _sports: Dict[str, SportConfig] = {
        "clavados": SportConfig(
            key="clavados",
            display_name="Diving",
            max_score=100.0,
            descriptor_focus=[
                "approach and hurdle: control, balance, and takeoff technique",
                "impulse generation: efficient use of springboard or platform",
                "height and distance: sufficient elevation and safe separation from board/platform",
                "aerial execution: body shape quality (straight, pike, tuck)",
                "aerial execution: clean twists and somersaults",
                "aerial execution: full control of movement from takeoff to entry",
                "water entry: vertical alignment",
                "water entry: minimal splash",
            ],
        )
    }

    @classmethod
    def get(cls, sport_key: str) -> SportConfig:
        normalized_key = sport_key.strip().lower()
        if normalized_key not in cls._sports:
            available = ", ".join(sorted(cls._sports.keys()))
            raise ValueError(
                f"Unsupported sport: {sport_key}. Available sports: {available}"
            )

        return cls._sports[normalized_key]

    @classmethod
    def available_sports(cls) -> List[str]:
        return sorted(cls._sports.keys())
