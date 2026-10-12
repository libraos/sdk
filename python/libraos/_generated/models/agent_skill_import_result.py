from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_skill_import_result_results_item import AgentSkillImportResultResultsItem


T = TypeVar("T", bound="AgentSkillImportResult")


@_attrs_define
class AgentSkillImportResult:
    """
    Attributes:
        repo (str):
        commit (str):
        license_ (str):
        results (list[AgentSkillImportResultResultsItem]): One entry per skill; per-skill failures are reported here.
    """

    repo: str
    commit: str
    license_: str
    results: list[AgentSkillImportResultResultsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repo = self.repo

        commit = self.commit

        license_ = self.license_

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repo": repo,
                "commit": commit,
                "license": license_,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_skill_import_result_results_item import AgentSkillImportResultResultsItem

        d = dict(src_dict)
        repo = d.pop("repo")

        commit = d.pop("commit")

        license_ = d.pop("license")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = AgentSkillImportResultResultsItem.from_dict(results_item_data)

            results.append(results_item)

        agent_skill_import_result = cls(
            repo=repo,
            commit=commit,
            license_=license_,
            results=results,
        )

        agent_skill_import_result.additional_properties = d
        return agent_skill_import_result

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
