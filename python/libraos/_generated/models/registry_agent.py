from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.registry_agent_model_source import RegistryAgentModelSource
from ..models.registry_agent_source import RegistryAgentSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.registry_agent_trust import RegistryAgentTrust


T = TypeVar("T", bound="RegistryAgent")


@_attrs_define
class RegistryAgent:
    """One agent as the registry has it loaded. Mirrors the admin surface's AgentSummary; optional fields are omitted
    rather than null.

        Example:
            {'agent_id': 'qc-legal-researcher', 'name': 'QC Legal Researcher', 'agent_type': 'persona', 'status': 'healthy',
                'source': 'custom', 'editable': True, 'model_override': 'anthropic/claude-sonnet-5', 'model': 'anthropic/claude-
                sonnet-5', 'model_source': 'agent', 'bound_collections_count': 2}

        Attributes:
            agent_id (str):
            name (str):
            agent_type (str): persona | skill
            status (str):  Example: healthy.
            source (RegistryAgentSource): `preset` ships with the release image; `custom` was created at runtime. A runtime
                file overriding a preset id reports `custom`, because the runtime file is what executes.
            editable (bool): False for an orphan — not in a managed pack directory.
            description (str | Unset):
            brain (bool | Unset): Retrieval/brain capability.
            capabilities (list[str] | Unset):
            tags (list[str] | Unset):
            pack_id (str | Unset):
            model_override (str | Unset): The model explicitly pinned in the agent's definition. ABSENT on bundled presets,
                which pin nothing — read `model` for what an agent will actually run on.
            model (str | Unset): The EFFECTIVE model: what this agent runs on, whether pinned or inherited. Absent when it
                cannot be determined, which is reported rather than guessed — a settings-in-database deployment can override the
                server default, and a confidently wrong answer to "what will this run on" is worse than none.
            model_source (RegistryAgentModelSource | Unset): Where `model` came from. Absent alongside an absent `model`.
            bound_collections_count (int | Unset):
            source_path (str | Unset):
            disabled (bool | Unset): Hidden from the model list while staying reachable by explicit id.
            loaded_skills (list[str] | Unset): Tool packs the agent has loaded.
            tool_count (int | Unset):
            trust (RegistryAgentTrust | Unset): Trust record; zero-valued when not scored.
    """

    agent_id: str
    name: str
    agent_type: str
    status: str
    source: RegistryAgentSource
    editable: bool
    description: str | Unset = UNSET
    brain: bool | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    tags: list[str] | Unset = UNSET
    pack_id: str | Unset = UNSET
    model_override: str | Unset = UNSET
    model: str | Unset = UNSET
    model_source: RegistryAgentModelSource | Unset = UNSET
    bound_collections_count: int | Unset = UNSET
    source_path: str | Unset = UNSET
    disabled: bool | Unset = UNSET
    loaded_skills: list[str] | Unset = UNSET
    tool_count: int | Unset = UNSET
    trust: RegistryAgentTrust | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        name = self.name

        agent_type = self.agent_type

        status = self.status

        source = self.source.value

        editable = self.editable

        description = self.description

        brain = self.brain

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        pack_id = self.pack_id

        model_override = self.model_override

        model = self.model

        model_source: str | Unset = UNSET
        if not isinstance(self.model_source, Unset):
            model_source = self.model_source.value

        bound_collections_count = self.bound_collections_count

        source_path = self.source_path

        disabled = self.disabled

        loaded_skills: list[str] | Unset = UNSET
        if not isinstance(self.loaded_skills, Unset):
            loaded_skills = self.loaded_skills

        tool_count = self.tool_count

        trust: dict[str, Any] | Unset = UNSET
        if not isinstance(self.trust, Unset):
            trust = self.trust.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_id": agent_id,
                "name": name,
                "agent_type": agent_type,
                "status": status,
                "source": source,
                "editable": editable,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if brain is not UNSET:
            field_dict["brain"] = brain
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if tags is not UNSET:
            field_dict["tags"] = tags
        if pack_id is not UNSET:
            field_dict["pack_id"] = pack_id
        if model_override is not UNSET:
            field_dict["model_override"] = model_override
        if model is not UNSET:
            field_dict["model"] = model
        if model_source is not UNSET:
            field_dict["model_source"] = model_source
        if bound_collections_count is not UNSET:
            field_dict["bound_collections_count"] = bound_collections_count
        if source_path is not UNSET:
            field_dict["source_path"] = source_path
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if loaded_skills is not UNSET:
            field_dict["loaded_skills"] = loaded_skills
        if tool_count is not UNSET:
            field_dict["tool_count"] = tool_count
        if trust is not UNSET:
            field_dict["trust"] = trust

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registry_agent_trust import RegistryAgentTrust

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        name = d.pop("name")

        agent_type = d.pop("agent_type")

        status = d.pop("status")

        source = RegistryAgentSource(d.pop("source"))

        editable = d.pop("editable")

        description = d.pop("description", UNSET)

        brain = d.pop("brain", UNSET)

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        pack_id = d.pop("pack_id", UNSET)

        model_override = d.pop("model_override", UNSET)

        model = d.pop("model", UNSET)

        _model_source = d.pop("model_source", UNSET)
        model_source: RegistryAgentModelSource | Unset
        if isinstance(_model_source, Unset):
            model_source = UNSET
        else:
            model_source = RegistryAgentModelSource(_model_source)

        bound_collections_count = d.pop("bound_collections_count", UNSET)

        source_path = d.pop("source_path", UNSET)

        disabled = d.pop("disabled", UNSET)

        loaded_skills = cast(list[str], d.pop("loaded_skills", UNSET))

        tool_count = d.pop("tool_count", UNSET)

        _trust = d.pop("trust", UNSET)
        trust: RegistryAgentTrust | Unset
        if isinstance(_trust, Unset):
            trust = UNSET
        else:
            trust = RegistryAgentTrust.from_dict(_trust)

        registry_agent = cls(
            agent_id=agent_id,
            name=name,
            agent_type=agent_type,
            status=status,
            source=source,
            editable=editable,
            description=description,
            brain=brain,
            capabilities=capabilities,
            tags=tags,
            pack_id=pack_id,
            model_override=model_override,
            model=model,
            model_source=model_source,
            bound_collections_count=bound_collections_count,
            source_path=source_path,
            disabled=disabled,
            loaded_skills=loaded_skills,
            tool_count=tool_count,
            trust=trust,
        )

        registry_agent.additional_properties = d
        return registry_agent

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
