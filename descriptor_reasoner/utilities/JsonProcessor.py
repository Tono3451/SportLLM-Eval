import json
from typing import Any, Dict, Optional


class JsonProcessor:
    @staticmethod
    def parse_json_response(raw_text: str) -> Optional[Dict[str, Any]]:
        if not raw_text:
            return None

        candidate = raw_text.strip()

        parsed = JsonProcessor._safe_json_loads(candidate)
        if parsed is not None:
            return parsed

        fenced = JsonProcessor._extract_fenced_block(candidate)
        if fenced:
            parsed = JsonProcessor._safe_json_loads(fenced)
            if parsed is not None:
                return parsed

        bracketed = JsonProcessor._extract_json_object(candidate)
        if bracketed:
            parsed = JsonProcessor._safe_json_loads(bracketed)
            if parsed is not None:
                return parsed

        return None

    @staticmethod
    def validate_descriptor_payload(payload: Dict[str, Any]) -> None:
        required_keys = {
            "sport",
            "action_name",
            "phases",
            "metrics",
            "faults",
            "confidence",
        }
        JsonProcessor._validate_required_keys(payload, required_keys, "descriptor")

        if not isinstance(payload["phases"], dict):
            raise ValueError("descriptor.phases debe ser un objeto JSON")

        phase_keys = {"setup", "execution", "recovery"}
        missing_phase_keys = phase_keys.difference(payload["phases"].keys())
        if missing_phase_keys:
            raise ValueError(
                f"descriptor.phases no contiene todas las fases requeridas: {sorted(missing_phase_keys)}"
            )

        if not isinstance(payload["faults"], list):
            raise ValueError("descriptor.faults debe ser una lista")

        JsonProcessor._validate_confidence(payload["confidence"], "descriptor.confidence")

    @staticmethod
    def validate_reasoner_payload(payload: Dict[str, Any], max_score: float) -> None:
        required_keys = {
            "sport",
            "rubric_version",
            "deductions",
            "score_raw",
            "score_final",
            "confidence",
            "justification_short",
        }
        JsonProcessor._validate_required_keys(payload, required_keys, "reasoner")

        if not isinstance(payload["deductions"], list):
            raise ValueError("reasoner.deductions debe ser una lista")

        score_raw = JsonProcessor._validate_numeric(payload["score_raw"], "reasoner.score_raw")
        score_final = JsonProcessor._validate_numeric(payload["score_final"], "reasoner.score_final")

        if score_raw < 0 or score_raw > max_score:
            raise ValueError(
                f"reasoner.score_raw fuera de rango [0, {max_score}]: {score_raw}"
            )

        if score_final < 0 or score_final > max_score:
            raise ValueError(
                f"reasoner.score_final fuera de rango [0, {max_score}]: {score_final}"
            )

        JsonProcessor._validate_confidence(payload["confidence"], "reasoner.confidence")

    @staticmethod
    def normalize_reasoner_payload(
        payload: Dict[str, Any],
        sport: str,
        rubric_version: str,
        max_score: float,
    ) -> Dict[str, Any]:
        normalized = dict(payload)

        if "sport" not in normalized:
            normalized["sport"] = sport

        if "rubric_version" not in normalized:
            normalized["rubric_version"] = rubric_version

        if "deductions" not in normalized:
            if isinstance(normalized.get("faults"), list):
                normalized["deductions"] = [
                    {
                        "code": fault.get("code", "UNKNOWN") if isinstance(fault, dict) else "UNKNOWN",
                        "points": fault.get("points", 0) if isinstance(fault, dict) else 0,
                        "rationale": fault.get("evidence", "Converted from descriptor fault") if isinstance(fault, dict) else "Converted from non-dict fault",
                    }
                    for fault in normalized.get("faults", [])
                ]
            else:
                normalized["deductions"] = []

        if "score_raw" not in normalized:
            alias_raw = JsonProcessor._first_present_key(
                normalized,
                ["score", "final_score", "finalScore", "scoreFinal", "overall_score"],
            )
            if alias_raw is not None:
                normalized["score_raw"] = alias_raw

        if "score_final" not in normalized:
            alias_final = JsonProcessor._first_present_key(
                normalized,
                ["final_score", "finalScore", "score", "scoreFinal", "overall_score"],
            )
            if alias_final is not None:
                normalized["score_final"] = alias_final

        if "confidence" not in normalized:
            alias_conf = JsonProcessor._first_present_key(
                normalized,
                ["confidence_score", "conf", "certainty"],
            )
            normalized["confidence"] = alias_conf if alias_conf is not None else 0.5

        if "justification_short" not in normalized:
            alias_just = JsonProcessor._first_present_key(
                normalized,
                ["justification", "rationale", "summary", "verdict"],
            )
            normalized["justification_short"] = (
                alias_just
                if alias_just is not None
                else "No justification provided by the model."
            )

        normalized["score_raw"] = JsonProcessor._coerce_and_clamp_score(
            normalized.get("score_raw"),
            max_score,
        )
        normalized["score_final"] = JsonProcessor._coerce_and_clamp_score(
            normalized.get("score_final"),
            max_score,
        )
        normalized["confidence"] = JsonProcessor._coerce_and_clamp_confidence(
            normalized.get("confidence"),
        )

        return normalized

    @staticmethod
    def _safe_json_loads(text: str) -> Optional[Dict[str, Any]]:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None

        return data

    @staticmethod
    def _extract_fenced_block(text: str) -> Optional[str]:
        fence_start = text.find("```")
        if fence_start < 0:
            return None

        first_line_end = text.find("\n", fence_start)
        if first_line_end < 0:
            return None

        fence_end = text.find("```", first_line_end + 1)
        if fence_end < 0:
            return None

        return text[first_line_end + 1:fence_end].strip()

    @staticmethod
    def _extract_json_object(text: str) -> Optional[str]:
        start = text.find("{")
        end = text.rfind("}")

        if start < 0 or end < 0 or end <= start:
            return None

        return text[start:end + 1]

    @staticmethod
    def _validate_required_keys(payload: Dict[str, Any], keys: set, prefix: str) -> None:
        missing = keys.difference(payload.keys())
        if missing:
            raise ValueError(f"{prefix} JSON incompleto, faltan claves: {sorted(missing)}")

    @staticmethod
    def _validate_confidence(value: Any, field_name: str) -> None:
        conf = JsonProcessor._validate_numeric(value, field_name)
        if conf < 0 or conf > 1:
            raise ValueError(f"{field_name} fuera de rango [0, 1]: {conf}")

    @staticmethod
    def _validate_numeric(value: Any, field_name: str) -> float:
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                pass

        raise ValueError(f"{field_name} debe ser numerico")

    @staticmethod
    def _first_present_key(payload: Dict[str, Any], keys: list) -> Any:
        for key in keys:
            if key in payload:
                return payload[key]
        return None

    @staticmethod
    def _coerce_and_clamp_score(value: Any, max_score: float) -> float:
        if value is None:
            return 0.0

        score = JsonProcessor._validate_numeric(value, "score")
        return max(0.0, min(float(max_score), score))

    @staticmethod
    def _coerce_and_clamp_confidence(value: Any) -> float:
        if value is None:
            return 0.5

        conf = JsonProcessor._validate_numeric(value, "confidence")
        return max(0.0, min(1.0, conf))
