from enum import Enum


class SkillRequestCandidateCatalog(str, Enum):
    NAME_TAKEN = "name_taken"
    NEW = "new"
    PUBLISHED = "published"

    def __str__(self) -> str:
        return str(self.value)
