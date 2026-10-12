from enum import Enum


class AgentOnAmbiguousEntity(str, Enum):
    ASK = "ask"
    OFF = "off"
    STATE = "state"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
