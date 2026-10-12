from enum import Enum


class AgentTriageDefaultBrain(str, Enum):
    ALWAYS = "always"
    NEVER = "never"
    TRIAGE = "triage"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
