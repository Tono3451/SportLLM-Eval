import json
from pathlib import Path
from typing import Any, Dict, TextIO


class FileProcessor:
	def __init__(self, file_path: str):
		self.file_path = Path(file_path)
		self.file_path.parent.mkdir(parents=True, exist_ok=True)
		self.file_handle: TextIO = self.file_path.open("a+", encoding="utf-8")

	def add_video_result(self, video_path: str, description: str, score: Any) -> Dict[str, Any]:
		record = {
			"video_path": video_path,
			"description": description,
			"score": score,
		}

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
