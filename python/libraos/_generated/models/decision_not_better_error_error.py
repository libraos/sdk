from enum import Enum


class DecisionNotBetterErrorError(str, Enum):
    CONFIDENCE_NOT_BETTER_THAN_PRIOR = "confidence_not_better_than_prior"

    def __str__(self) -> str:
        return str(self.value)
