from enum import Enum


class AgentSkillFileDiffChange(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    REMOVED = "removed"

    def __str__(self) -> str:
        return str(self.value)
