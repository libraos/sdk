from enum import Enum


class AgentToolScope(str, Enum):
    NONE = "none"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
