from enum import Enum


class GetModelRecommendationsCompatibility(str, Enum):
    INCOMPATIBLE = "incompatible"
    POTENTIALLY_COMPATIBLE = "potentially_compatible"
    VALIDATED_MATCH = "validated_match"

    def __str__(self) -> str:
        return str(self.value)
