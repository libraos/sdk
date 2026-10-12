from enum import Enum


class ChatCompletionRequestMetadataResearchDepth(str, Enum):
    AUTO = "auto"
    DEEP = "deep"
    FAST = "fast"

    def __str__(self) -> str:
        return str(self.value)
