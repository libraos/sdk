from enum import Enum


class MessageRequestMetadataResearchDepth(str, Enum):
    AUTO = "auto"
    DEEP = "deep"
    FAST = "fast"

    def __str__(self) -> str:
        return str(self.value)
