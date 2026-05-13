from pathlib import Path
from typing import Any

import h5py
import numpy as np
from scipy.io import loadmat


class MatProcessor:
    @staticmethod
    def get_score(mat_path: str, index: int, variable_name: str | None = None) -> float:
        try:
            if index < 1:
                return 0.0

            path = Path(mat_path)
            if not path.exists() or not path.is_file():
                return 0.0

            candidates = MatProcessor._load_candidates(path, variable_name)

            for candidate in candidates:
                value = MatProcessor._extract_indexed_value(candidate, index)
                if value is not None:
                    return value

            return 0.0
        except Exception:
            return 0.0

    @staticmethod
    def _candidate_variables(data: dict[str, Any], variable_name: str | None) -> list[Any]:
        if variable_name:
            return [data.get(variable_name)] if variable_name in data else []

        return [
            value
            for key, value in data.items()
            if not key.startswith("__")
        ]

    @staticmethod
    def _load_candidates(path: Path, variable_name: str | None) -> list[Any]:
        try:
            data = loadmat(path, squeeze_me=True, struct_as_record=False)
            return MatProcessor._candidate_variables(data, variable_name)
        except Exception:
            return MatProcessor._load_candidates_v73(path, variable_name)

    @staticmethod
    def _load_candidates_v73(path: Path, variable_name: str | None) -> list[Any]:
        try:
            with h5py.File(path, "r") as handle:
                if variable_name:
                    if variable_name not in handle:
                        return []
                    return [handle[variable_name][()]]

                return [handle[key][()] for key in handle.keys()]
        except Exception:
            return []

    @staticmethod
    def _extract_indexed_value(candidate: Any, index: int) -> float | None:
        if candidate is None:
            return None

        try:
            array = np.asarray(candidate).squeeze()
            if array.size == 0:
                return None

            flat = array.reshape(-1)
            zero_based_index = index - 1
            if zero_based_index < 0 or zero_based_index >= flat.size:
                return None

            value = flat[zero_based_index]
            if isinstance(value, np.ndarray):
                value = value.squeeze()
                if np.size(value) == 0:
                    return None
                value = value.item()

            return float(value)
        except Exception:
            return None
