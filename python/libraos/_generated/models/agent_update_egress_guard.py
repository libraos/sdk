from enum import Enum


class AgentUpdateEgressGuard(str, Enum):
    CALLBACK = "callback"
    DETECTOR = "detector"
    OFF = "off"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
