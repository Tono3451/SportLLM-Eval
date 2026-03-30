class GenericPrompt:
    def __init__(self, system, user):
        self.system = system
        self.user = user

    def getUserPrompt(self):
        return self.system
    
    def getSystemPrompt(self):
        return self.user
        

class DescriptorPrompt:
    system_prompt = """## ROLE
You are a Senior Sports Performance Analyst and Technical Judge. Your goal is to deconstruct sports movements into high-precision technical data points for later scoring and kinematic analysis.

## OBJECTIVE
Generate a frame-by-frame technical breakdown of the athletic performance. Your description must be so precise that a judge could assign a score WITHOUT seeing the video, relying only on your text.

## NARRATION STRUCTURE
For every distinct movement, follow the "Triple-A" rule:
1. ACTION: Exact technical name of the maneuver.
2. ANATOMY: Body alignment, joint angles (e.g., "knees at 90 degrees"), and limb extension.
3. AXIS: Rotation count, direction, and spatial trajectory.

## MANDATORY INSTRUCTIONS:
- Use "Phase-Based Labeling": Divide the clip into (1) Initial Setup, (2) Execution/Flight, and (3) Recovery/Landing.
- Quantification: Instead of "many rotations," use "approximately 720 degrees of rotation." Instead of "high jump," use "maximum vertical extension relative to the athlete's height."
- Precision: Describe the 'Form Error' if any (e.g., "unpointed toes," "slight arch in the lower back," "asymmetric arm placement").
- Granularity: One technical observation per sentence. Avoid adjectives like "beautiful" or "great"; use "stable," "fluid," or "aligned."

## QUERY COMPLIANCE:
Your description must provide data to answer:
- What was the exact degree of limb extension at the peak of the action?
- Was the center of gravity maintained during the transition?
- Identify the exact moment of loss of balance or technical deviation."""
    
    user_prompt_description = """The following is the technical log generated so far: 

{Description}

CONTINUATION TASK: Observe the new frames provided. Maintain the same technical tone and granularity. Ensure the transition between the previous state and the current action is seamless. Describe the next sequence of movements starting from the last known position:"""
    
    user_prompt = "Analyze the provided visual data. Following the Biomechanics Analyst protocol, perform a step-by-step technical deconstruction of the athletic performance shown. Focus on joint alignment and phase transitions. Start the technical narration now:"

    description=""

    def __init__(self, enableHistory):
        self.enableHistory = enableHistory

    def addDescription(self, description):
        self.description += f"\n"
        self.description += description

    def getUserPrompt(self):
        if (self.enableHistory):
            temp = self.user_prompt_description.format(
                Description=self.description
            )
        else:
            temp = self.user_prompt

        return temp
    
    def getSystemPrompt(self):
        return self.system_prompt
    