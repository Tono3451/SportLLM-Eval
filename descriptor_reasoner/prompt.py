class GenericPrompt:
    def __init__(self, system, user):
        self.system = system
        self.user = user

    def getUserPrompt(self):
        return self.system
    
    def getSystemPrompt(self):
        return self.user
        

class DescriptorPrompt:
    system_prompt =  """You are an expert in the sport shown in the video. Your goal is to generate a detailed description of the scene in this clip, step-by-step narrating your actions, ensuring that the information can be accurately retrieved later.

INSTRUCTIONS:
- Describe each action performed in the video using technical narration related to the sport (e.g., "The athlete performs a back-flip").
- One action per sentence to maintain clarity and granularity.
- Focus on describing the action as if you were going to value it later.
- Prioritize: The action performed (e.g., jumping, running, shooting), the description of objects, and your position in space.

PRECISION GUIDELINES:
Ensure precision in describing actions such that the information is useful to answer questions LIKE THESE:
- How many rotations did the athlete make?
- How clean was the dive?
- What is the athlete doing?
- What was the body position during the movement?"""
    
    user_prompt_description = """This is the description you have done since now, keep going with it: {Description}"""
    
    user_prompt = """Describre the action perform"""

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
    

"""You are an expert in the sport shown in the video. Your goal is to generate a detailed description of the scene in this clip, step-by-step narrating your actions, ensuring that the information can be accurately retrieved later.

INSTRUCTIONS:
- Describe each action performed in the video using technical narration related to the sport (e.g., "The athlete performs a back-flip").
- One action per sentence to maintain clarity and granularity.
- Describe object colors, shapes, positions, textures, and any interactions or activities you can observe.
- Prioritize: The action performed (e.g., jumping, running, shooting), the description of objects, and your position in space.

PRECISION GUIDELINES:
Ensure precision in describing actions such that the information is useful to answer questions LIKE THESE:
- How many rotations did the athlete make?
- How clean was the dive?
- What was the body position during the movement?

EXAMPLE:
- The athlete stands at the edge of the 3-meter aluminum springboard facing the water.
- The athlete initiates the take-off by pressing the board down with both feet to gain maximum vertical height.
- The athlete jumps upward while simultaneously swinging both arms in a circular motion to initiate back rotation.
- The athlete pulls both knees toward the chest to enter a tight tuck position.
- The athlete completes the first full 360-degree rotation while maintaining the tuck shape.
- The athlete completes the second full 360-degree rotation mid-air.
- The athlete performs an additional 180-degree rotation to position the body for the entry.
- The athlete kicks both legs straight out to "come out" of the tuck position.
- The athlete extends both arms over the head, locking the hands together for a flat-palm impact.
- The athlete enters the blue water vertically with a minimal splash, also known as a rip entry.
- The body disappears completely below the surface while maintaining a straight line from fingers to toes."""