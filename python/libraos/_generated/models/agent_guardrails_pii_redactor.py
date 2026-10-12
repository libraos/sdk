from enum import Enum


class AgentGuardrailsPiiRedactor(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
