from enum import Enum


class AgentGuardrailsDateNormalizer(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
