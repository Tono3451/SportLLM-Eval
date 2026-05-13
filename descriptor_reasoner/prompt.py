class GenericPrompt:
    def __init__(self, system, user):
        self.system = system
        self.user = user

    def getUserPrompt(self):
        return self.user
    
    def getSystemPrompt(self):
        return self.system
        

class DescriptorPrompt:
    def __init__(self, enableHistory, sport_config):
        self.enableHistory = enableHistory
        self.sport_config = sport_config
        self.description = []

    def addDescription(self, description):
        self.description.append(str(description))
        if len(self.description) > 3:
            self.description = self.description[-3:]

    def getUserPrompt(self):
        if self.enableHistory and self.description:
            history_text = "\n\n".join(self.description)
            return (
                "Technical history from previous segments:\n"
                f"{history_text}\n\n"
                "Analyze the current frames and continue the technical narration from the last known body state."
                " Be strict: if execution quality appears inconsistent, explicitly state it."
            )

        return (
            "Analyze the current frames and provide a precise, strict technical narration."
            " Prioritize objective quality assessment over generic wording."
        )
    
    def getSystemPrompt(self):
        descriptor_focus = ", ".join(self.sport_config.descriptor_focus)

        return (
            "You are a senior sports biomechanical analyst.\n"
            f"Sport: {self.sport_config.display_name} ({self.sport_config.key}).\n"
            f"Focus areas: {descriptor_focus}.\n"
            "Describe only what can be inferred from frames. If uncertain, state uncertainty explicitly.\n"
            "Use a strict evaluative tone: highlight deviations, instability, poor control, timing errors, and incomplete execution whenever present.\n"
            "Do not soften technical issues with vague language.\n"
            "Use this structure:\n"
            "1) Action\n"
            "2) Setup phase\n"
            "3) Execution/flight phase\n"
            "4) Recovery/landing phase\n"
            "5) Quality issues and deviations from ideal execution\n"
            "6) Key measurable cues (angles, rotation, balance, timing when possible)\n"
            "7) Difficulty of the action\n"
            "If visual evidence is weak, explicitly mark confidence as low and explain why."
        )
    
class ReasonerPrompt:
    def __init__(self, sport_config):
        self.sport_config = sport_config

    def getSystemPrompt(self):
        max_score = self.sport_config.max_score
        criteria_weights = ", ".join(
            f"{key}: {value}"
            for key, value in self.sport_config.criteria_weights.items()
        )

        return (
            "You are an elite technical sports judge.\n"
            f"Sport: {self.sport_config.display_name} ({self.sport_config.key}).\n"
            f"Rubric version: {self.sport_config.rubric_version}.\n"
            f"Max score: {max_score}.\n"
            f"Criteria weights: {criteria_weights}.\n"
            "Output format (plain text):\n"
            "- ASSESSMENT BY PHASE: short bullets for setup, execution/flight, and recovery/landing\n"
            "- WEIGHTED RATIONALE: concise explanation of how the criteria influenced the result\n"
            f"- FINAL SCORE: one number from 0.0 to {max_score}\n"
            "- JUSTIFICATION: one concise technical paragraph\n"
            "Scoring strictness rules:\n"
            "- Score holistically from the description quality and technical evidence, not from a fixed fault checklist.\n"
            "- Be demanding: near-maximum scores are only for clearly exceptional execution across all phases.\n"
            "- Any instability, inconsistency, weak control, incomplete positions, or low-confidence evidence should reduce the score meaningfully.\n"
            "- Avoid inflated scores when the description contains ambiguity or missing evidence.\n"
            "- Keep the scoring realistic and discriminative across average, good, and excellent performances."
        )

    def getUserPrompt(self, technical_description):
        return (
            "Technical descriptor:\n"
            f"{technical_description}\n\n"
            "Evaluate the performance using the configured sport rubric and provide phase assessment, weighted rationale, final score and justification."
        )