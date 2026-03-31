from descriptor_reasoner.ActionScorer import ActionScorer
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels
from descriptor_reasoner.reasoner.ReasonerModels import ReasonerModels
from descriptor_reasoner.prompt import DescriptorPrompt, GenericPrompt, ReasonerPrompt
from descriptor_reasoner.utilities.ImageProcessor import _resize_calculation

def main():
    descriptor_prompt = DescriptorPrompt(False)
    reason_prompt = ReasonerPrompt()


    actionScorer = ActionScorer(
                                r"C:\Users\Tono3451\tft-pruebas\video\057.mp4",
                                DescriptorModels.QWEN2_5VL_3B,
                                ReasonerModels.DEEPSEEK_R1_7B,
                                3,
                                16,
                                320
                            )

    print(actionScorer.scoreAction(descriptor_prompt, reason_prompt, True))

if __name__ == "__main__":
    main()