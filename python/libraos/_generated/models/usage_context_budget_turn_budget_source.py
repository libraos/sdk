from enum import Enum


class UsageContextBudgetTurnBudgetSource(str, Enum):
    AGENT = "agent"
    ENV = "env"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
