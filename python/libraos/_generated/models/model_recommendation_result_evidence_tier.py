from enum import Enum


class ModelRecommendationResultEvidenceTier(str, Enum):
    INDICATIVE = "indicative"
    NONE = "none"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
