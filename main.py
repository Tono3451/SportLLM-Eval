from descriptor_reasoner.ActionScorer import ActionScorer
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels
from descriptor_reasoner.reasoner.ReasonerModels import ReasonerModels
from descriptor_reasoner.prompt import DescriptorPrompt, ReasonerPrompt
from descriptor_reasoner.sports_catalog import SportsCatalog
from descriptor_reasoner.utilities.MatProcessor import MatProcessor
from descriptor_reasoner.utilities.FileProcessor import FileProcessor
from pathlib import Path
import re

SPORT_KEY = "clavados"

# Modos disponibles: "single", "all", "subset", "range"
PROCESS_MODE = "range"

VIDEO_PATH = r"D:\clase\tft\dataset\diving\diving\diving_samples_len_ori\001.avi"
VIDEO_DIRECTORY = r"D:\clase\tft\dataset\diving\diving\diving_samples_len_ori"
SUBSET_INDICES = [1, 2, 3]
START_INDEX = 1
END_INDEX = 4

OUTPUT_FILE = r"C:\Users\Tono3451\tft-pruebas\results\clavados3.jsonl"
MAT_FILE_PATH = r"D:\clase\tft\dataset\diving\diving\diving_overall_scores.mat"
MAT_SCORE_INDEX = None

DESCRIPTOR_MODEL = DescriptorModels.QWEN2_5VL_3B
REASONER_MODEL = ReasonerModels.DEEPSEEK_R1_7B
DESCRIPTION_SECONDS = 2
FRAMES_PER_SEGMENT = 24
MAX_PIXEL_SIZE = 448

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}


def extract_video_index(video_path: Path) -> int | None:
    stem = video_path.stem.strip()
    if stem.isdigit():
        return int(stem)

    matches = re.findall(r"\d+", stem)
    if not matches:
        return None

    return int(matches[-1])


def list_videos_in_folder(folder_path: str) -> list[Path]:
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []

    video_paths = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    ]

    def sort_key(path: Path):
        idx = extract_video_index(path)
        if idx is None:
            return (1, path.name.lower())
        return (0, idx)

    return sorted(video_paths, key=sort_key)


def resolve_video_paths() -> list[Path]:
    mode = PROCESS_MODE.strip().lower()

    if mode == "single":
        path = Path(VIDEO_PATH)
        return [path] if path.exists() and path.is_file() else []

    all_videos = list_videos_in_folder(VIDEO_DIRECTORY)

    if mode == "all":
        return all_videos

    if mode == "subset":
        target_indices = set(SUBSET_INDICES)
        return [
            path
            for path in all_videos
            if (extract_video_index(path) in target_indices)
        ]

    if mode == "range":
        min_idx = min(START_INDEX, END_INDEX)
        max_idx = max(START_INDEX, END_INDEX)
        selected = []
        for path in all_videos:
            idx = extract_video_index(path)
            if idx is not None and min_idx <= idx <= max_idx:
                selected.append(path)
        return selected

    print(f"PROCESS_MODE no soportado: {PROCESS_MODE}. Usa single, all, subset o range")
    return []


def resolve_real_score_index(video_path: Path) -> int | None:
    if MAT_SCORE_INDEX is not None:
        return MAT_SCORE_INDEX

    return extract_video_index(video_path)


def main():
    try:
        sport_config = SportsCatalog.get(SPORT_KEY)
    except ValueError as exc:
        print(exc)
        print(f"Deportes disponibles: {SportsCatalog.available_sports()}")
        return

    videos = resolve_video_paths()
    if not videos:
        print("No se encontraron videos para procesar con la configuracion actual")
        return

    with FileProcessor(OUTPUT_FILE) as file_processor:
        for video_path in videos:
            descriptor_prompt = DescriptorPrompt(True, sport_config)
            reason_prompt = ReasonerPrompt(sport_config)

            action_scorer = ActionScorer(
                str(video_path),
                DESCRIPTOR_MODEL,
                REASONER_MODEL,
                DESCRIPTION_SECONDS,
                FRAMES_PER_SEGMENT,
                MAX_PIXEL_SIZE,
            )

            description = action_scorer.describeVideo(descriptor_prompt)
            score = action_scorer.reasonDescription(reason_prompt, description)

            mat_index = resolve_real_score_index(video_path)
            real_score = 0.0
            if MAT_FILE_PATH and mat_index is not None:
                real_score = MatProcessor.get_score(MAT_FILE_PATH, mat_index)

            file_processor.add_video_result(str(video_path), description, score, real_score)
            print(f"Procesado: {video_path.name} | indice MAT: {mat_index} | real score: {real_score}")

if __name__ == "__main__":
    main()