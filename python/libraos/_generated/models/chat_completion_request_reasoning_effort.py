from enum import Enum


class ChatCompletionRequestReasoningEffort(str, Enum):
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"
    NONE = "none"
    OFF = "off"
    VALUE_0 = ""
    XHIGH = "xhigh"

    def __str__(self) -> str:
        return str(self.value)
