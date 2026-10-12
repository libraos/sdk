from enum import Enum


class ScheduleLimitErrorError(str, Enum):
    SCHEDULE_LIMIT_REACHED = "schedule_limit_reached"

    def __str__(self) -> str:
        return str(self.value)
