from enum import Enum


class AgentSkillSourceKind(str, Enum):
    EDIT = "edit"
    GITHUB = "github"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
