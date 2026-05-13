from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class SportConfig:
    key: str
    display_name: str
    rubric_version: str
    max_score: float
    criteria_weights: Dict[str, float]
    descriptor_focus: List[str]


class SportsCatalog:
    _sports: Dict[str, SportConfig] = {
        "gimnasia_artistica": SportConfig(
            key="gimnasia_artistica",
            display_name="Artistic Gymnastics",
            rubric_version="1.0",
            max_score=100.0,
            criteria_weights={
                "technique": 0.45,
                "execution": 0.35,
                "landing": 0.20,
            },
            descriptor_focus=[
                "joint alignment",
                "rotation axis control",
                "landing quality",
            ],
        ),
        "clavados": SportConfig(
            key="clavados",
            display_name="Diving",
            rubric_version="1.0",
            max_score=100.0,
            criteria_weights={
                "takeoff": 0.25,
                "flight": 0.45,
                "entry": 0.30,
            },
            descriptor_focus=[
                "takeoff height and control",
                "body form during flight",
                "entry verticality and splash control",
            ],
        ),
        "patinaje_artistico": SportConfig(
            key="patinaje_artistico",
            display_name="Figure Skating",
            rubric_version="1.0",
            max_score=100.0,
            criteria_weights={
                "technique": 0.50,
                "stability": 0.30,
                "control": 0.20,
            },
            descriptor_focus=[
                "jump entry and exit",
                "axis alignment during spins",
                "landing stability",
            ],
        ),
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
