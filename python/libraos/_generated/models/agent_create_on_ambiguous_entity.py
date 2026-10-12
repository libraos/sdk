from enum import Enum


class AgentCreateOnAmbiguousEntity(str, Enum):
    ASK = "ask"
    OFF = "off"
    STATE = "state"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
