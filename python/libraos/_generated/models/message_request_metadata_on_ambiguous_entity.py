from enum import Enum


class MessageRequestMetadataOnAmbiguousEntity(str, Enum):
    ASK = "ask"
    OFF = "off"
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
