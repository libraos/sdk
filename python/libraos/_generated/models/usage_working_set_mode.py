from enum import Enum


class UsageWorkingSetMode(str, Enum):
    FULL = "full"
    MANIFEST = "manifest"

    def __str__(self) -> str:
        return str(self.value)
