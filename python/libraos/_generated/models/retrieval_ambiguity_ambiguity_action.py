from enum import Enum


class RetrievalAmbiguityAmbiguityAction(str, Enum):
    ASK = "ask"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
