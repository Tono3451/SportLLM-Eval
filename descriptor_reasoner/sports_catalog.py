from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SportConfig:
    key: str
    display_name: str
    max_score: float
    descriptor_focus: List[str]
    score_focus: List[str]
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
            score_focus=None
        ),
        "salto_potro": SportConfig(
            key="salto_potro",
            display_name="Gym Vault",
            max_score=0, # se calcula (D-score + E-score - Penalizaciones)
            descriptor_focus=[
                "run-up: speed generation, rhythm, and control during approach",
                "board contact: explosive and efficient takeoff from springboard",
                "pre-flight phase: body alignment and controlled table approach",
                "table contact: powerful block and shoulder extension",
                "post-flight phase: height, distance, and amplitude after table push-off",
                "aerial execution: body shape quality (tuck, pike, layout)",
                "aerial execution: clean twists and somersaults with precise form",
                "aerial execution: body tension, posture, and movement control throughout flight",
                "landing: stability, balance, and precise foot placement",
                "landing: minimal hops, steps, or body instability on impact",
                "vault aproximation: try to adjust the jump to a know vault"
            ],
            score_focus=[
                "The final score should follow the FIG-style formula: Final Score = D-Score + E-Score.",
                "Calculate the D-Score by approximating the performed vault to a known FIG vault family and estimating its official difficulty value.",
                "Calculate the E-Score starting from 10.0 and progressively applying execution deductions.",
                "Apply deductions for steps, hops, balance corrections, deep squats, arm swings, hand support, or falls on landing.",
                "Apply deductions for bent knees, leg separation, flexed feet, poor body alignment, or loose posture during flight.",
                "Apply deductions for insufficient height, weak table repulsion, low amplitude, or poor distance from the vault table.",
                "Apply deductions for incomplete twists, under-rotation, over-rotation, or uncontrolled aerial movement.",
                "Reward explosive table block, strong amplitude, high flight trajectory, and clear body control by minimizing execution deductions.",
                "Reward clean and recognizable vault structure matching a valid FIG vault family.",
                "Assign near-maximum scores only to vaults showing elite-level difficulty, exceptional execution quality, excellent amplitude, and near-perfect landing control.",
                "Avoid inflated scores when the descriptor contains ambiguity, inconsistent movement descriptions, missing technical evidence, or unclear vault identification.",
                "Differentiate clearly between low-quality, average, strong, and elite vault performances using realistic score separation.",
                "Finally, combine the estimated D-Score and E-Score into a realistic final vault score.",
                "There is no limit on the score points"
            ]
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
