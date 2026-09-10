from enum import Enum


class NativeChatResultGrounding(str, Enum):
    DEGRADED = "degraded"
    DEGRADED_RETRIEVAL = "degraded_retrieval"
    GROUNDED = "grounded"
    UNGROUNDED_NO_CHUNKS = "ungrounded_no_chunks"
    UNGROUNDED_REFUSAL = "ungrounded_refusal"
    UNOPENED_SOURCES = "unopened_sources"
    UNSUPPORTED_CLAIM = "unsupported_claim"

    def __str__(self) -> str:
        return str(self.value)
