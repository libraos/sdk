from enum import Enum


class AgentCreateEgressGuard(str, Enum):
    CALLBACK = "callback"
    DETECTOR = "detector"
    OFF = "off"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
