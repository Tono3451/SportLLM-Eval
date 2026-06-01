import json
from pathlib import Path
from typing import Any, Dict, TextIO


class FileProcessor:
	def __init__(self, file_path: str):
		self.file_path = Path(file_path)
		self.file_path.parent.mkdir(parents=True, exist_ok=True)
		self.file_handle: TextIO = self.file_path.open("a+", encoding="utf-8")

	def add_video_result(self, video_path: str, description: Any, score: Any, real_score: float = 0.0) -> Dict[str, Any]:
		record = {
			"video_path": video_path,
			"description": description,
			"score": score,
			"real_score": real_score,
		}

		if isinstance(description, dict):
			record["descriptor_json"] = description
			record["sport"] = description.get("sport")

		if isinstance(score, dict):
			record["reasoner_json"] = score
			record["score_final_num"] = score.get("score_final")
			if not record.get("sport"):
				record["sport"] = score.get("sport")

		if record.get("real_score") is None:
			record["real_score"] = 0.0

		self.file_handle.write(json.dumps(record, ensure_ascii=False) + "\n")
		self.file_handle.flush()
		return record

	def close(self) -> None:
		if not self.file_handle.closed:
			self.file_handle.close()

	def __enter__(self) -> "FileProcessor":
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		self.close()
