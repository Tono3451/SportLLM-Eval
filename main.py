from descriptor_reasoner.ActionScorer import ActionScorer
from descriptor_reasoner.descriptor.DescriptorModels import DescriptorModels
from descriptor_reasoner.prompt import DescriptorPrompt, GenericPrompt
from descriptor_reasoner.utilities.ImageProcessor import _resize_calculation

def main():
    prompt = DescriptorPrompt(False)

    actionScorer = ActionScorer(
                                r"C:\Users\Tono3451\tft-pruebas\video\057.mp4",
                                DescriptorModels.LLAVA_7B,
                                None,
                                3,
                                16,
                                320
                            )

    print(actionScorer.describeVideo(prompt))

if __name__ == "__main__":
    main()