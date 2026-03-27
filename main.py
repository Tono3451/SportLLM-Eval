from descriptor_reasoner.ActionScorer import ActionScorer
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels
from descriptor_reasoner.prompt import DescriptorPrompt

def main():
    prompt = DescriptorPrompt("A person doing trampoline jump",
                              "trampoline jump competition, camera at the right of the jumper")

    actionScorer = ActionScorer(
                                r"C:\Users\Tono3451\tft-pruebas\video\057.avi",
                                DescriptorModels.QWEN2_5VL_3B,
                                None,
                            )

    print(actionScorer.describeVideo(prompt))

if __name__ == "__main__":
    main()