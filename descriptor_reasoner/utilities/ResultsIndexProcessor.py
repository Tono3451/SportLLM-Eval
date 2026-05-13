import json
from pathlib import Path
from typing import List, Dict


class ResultsIndexProcessor:
    @staticmethod
    def build_index(results_dir: str) -> List[Dict[str, str]]:
        folder = Path(results_dir)
        if not folder.exists() or not folder.is_dir():
            return []

        items: List[Dict[str, str]] = []
        for file_path in sorted(folder.glob("*.jsonl")):
            if file_path.name.lower() == "index.json":
                continue
            items.append(
                {
                    "file_name": file_path.name,
                    "file_path": file_path.as_posix(),
                    "label": file_path.stem,
                }
            )
        return items

    @staticmethod
    def write_index(results_dir: str, index_file_name: str = "index.json") -> str:
        folder = Path(results_dir)
        folder.mkdir(parents=True, exist_ok=True)
        index_path = folder / index_file_name
        items = ResultsIndexProcessor.build_index(results_dir)
        index_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(index_path)
