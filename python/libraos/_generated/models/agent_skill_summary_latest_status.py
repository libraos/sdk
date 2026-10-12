from enum import Enum


class AgentSkillSummaryLatestStatus(str, Enum):
    ARCHIVED = "archived"
    DRAFT = "draft"
    PUBLISHED = "published"

    def __str__(self) -> str:
        return str(self.value)
