from enum import Enum


class UsageContextBudgetWindowSource(str, Enum):
    CATALOG = "catalog"
    ENV = "env"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
