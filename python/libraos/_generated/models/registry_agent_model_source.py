from enum import Enum


class RegistryAgentModelSource(str, Enum):
    AGENT = "agent"
    SERVER_DEFAULT = "server_default"

    def __str__(self) -> str:
        return str(self.value)
