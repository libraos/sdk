from enum import Enum


class ListRegistryAgentsSource(str, Enum):
    CUSTOM = "custom"
    PRESET = "preset"

    def __str__(self) -> str:
        return str(self.value)
