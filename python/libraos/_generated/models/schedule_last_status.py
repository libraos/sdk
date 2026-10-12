from enum import Enum


class ScheduleLastStatus(str, Enum):
    CANCELLED = "cancelled"
    CLAIMED = "claimed"
    DELIVERED = "delivered"
    DELIVERING = "delivering"
    FAILED = "failed"
    ORG_UNRECORDED = "org_unrecorded"
    OWNER_INACTIVE = "owner_inactive"
    PAUSED_FAILURES = "paused_failures"
    SKIPPED = "skipped"
    SUBMITTED = "submitted"
    VALUE_0 = ""

    def __str__(self) -> str:
        return str(self.value)
