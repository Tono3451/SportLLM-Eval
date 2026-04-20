from descriptor_reasoner.ActionScorer import ActionScorer
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels
from descriptor_reasoner.reasoner.ReasonerModels import ReasonerModels
from descriptor_reasoner.prompt import DescriptorPrompt, ReasonerPrompt
from descriptor_reasoner.utilities.FileProcessor import FileProcessor
from pathlib import Path

def main():
    descriptor_prompt = DescriptorPrompt(True)
    reason_prompt = ReasonerPrompt()

    video_directory = Path(r"C:\Users\Tono3451\tft-pruebas\video")
    video_paths = sorted(
        str(video_path)
        for video_path in video_directory.iterdir()
        if video_path.is_file() and video_path.suffix.lower() in {".mp4", ".mkv", ".avi", ".mov", ".webm"}
    )

    output_file = r"C:\Users\Tono3451\tft-pruebas\results\video_results.jsonl"

    with FileProcessor(output_file) as file_processor:
        for video_path in video_paths:
            action_scorer = ActionScorer(
                video_path,
                DescriptorModels.QWEN2_5VL_3B,
                ReasonerModels.DEEPSEEK_R1_7B,
                3,
                16,
                320,
            )

            description = action_scorer.describeVideo(descriptor_prompt)
            score = action_scorer.reasonDescription(reason_prompt, description)

            file_processor.add_video_result(video_path, description, score)
            print(score)

    

if __name__ == "__main__":
    main()