from enum import Enum


class AgentUpdateOnAmbiguousEntity(str, Enum):
    ASK = "ask"
    OFF = "off"
    STATE = "state"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
