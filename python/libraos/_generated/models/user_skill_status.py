from enum import Enum


class UserSkillStatus(str, Enum):
    ACTIVE = "active"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
