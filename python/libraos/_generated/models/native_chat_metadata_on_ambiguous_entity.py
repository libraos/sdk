from enum import Enum


class NativeChatMetadataOnAmbiguousEntity(str, Enum):
    ASK = "ask"
    OFF = "off"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
