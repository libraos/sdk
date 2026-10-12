from enum import Enum


class ModelRecommendationResultMatchedBy(str, Enum):
    HARDWARE_TABLE = "hardware_table"
    REQUIREMENTS = "requirements"

    def __str__(self) -> str:
        return str(self.value)
