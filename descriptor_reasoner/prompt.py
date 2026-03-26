class DescriptorPrompt:
    system_prompt =  """
        You are a professional video analyst. Your goal is to provide a highly 
        technical and objective description of the movements captured in the video.
        Focus on:
        1. Body mechanics (posture, limbs, speed).
        2. Spatial context (environment, objects involved).
        3. Temporal sequence (what happens first, then what).
        """
    
    user_prompt = """
        Analyze this video segment.
        Target Action: {action}
        Contextual Info: {context}

        Instruction: Provide a detailed breakdown of the action. 
        Do not give a score yet, just describe the raw data.
        """

    def __init__(self, action, context):
        self.action = action
        self.context = context

    def setAction(self, action):
        self.action = action

    def setContext(self, context):
        self.context = context

    def getUserPrompt(self):
        return self.system_prompt
    
    def getSystemPrompt(self):
        temp = self.system_prompt.format(
            action=self.action,
            context=self.context
        )

        return temp