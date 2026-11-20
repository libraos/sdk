from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.skill_request_candidate_catalog import SkillRequestCandidateCatalog
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.skill_request_left_out import SkillRequestLeftOut


T = TypeVar("T", bound="SkillRequestCandidate")


@_attrs_define
class SkillRequestCandidate:
    """One skill the link yields at the previewed commit, as an approval would import it. When `error` is set the skill
    cannot be imported and only `name` (if readable), `path` and `left_out` may be present.

        Attributes:
            path (str): The skill's folder in the repository.
            name (str | Unset):
            description (str | Unset):
            body (str | Unset): The instructions, `SKILL.md` without its frontmatter.
            sha256 (str | Unset): Digest over the files an approval imports, computed as for a catalog version.
            files (list[str] | Unset): Reference files an approval imports besides `SKILL.md`.
            left_out (list[SkillRequestLeftOut] | Unset): Files an approval leaves out: scripts (anything under `scripts/`,
                source and executable files, files starting with `#!`) and binary files. LibraOS never runs a skill's scripts.
            error (str | Unset):
            catalog (SkillRequestCandidateCatalog | Unset): What approving does to the org catalog. `new`: the skill is
                imported and published. `published`: identical content is already published as `catalog_version` and is reused.
                `name_taken`: the org already uses the name (a catalog version in any status, or a `LIBRA_OS_SKILLS_DIR`
                folder), so approving is refused with 409.
            catalog_version (int | Unset): The published version an approval would reuse, when `catalog` is `published`.
    """

    path: str
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    body: str | Unset = UNSET
    sha256: str | Unset = UNSET
    files: list[str] | Unset = UNSET
    left_out: list[SkillRequestLeftOut] | Unset = UNSET
    error: str | Unset = UNSET
    catalog: SkillRequestCandidateCatalog | Unset = UNSET
    catalog_version: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        name = self.name

        description = self.description

        body = self.body

        sha256 = self.sha256

        files: list[str] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = self.files

        left_out: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.left_out, Unset):
            left_out = []
            for left_out_item_data in self.left_out:
                left_out_item = left_out_item_data.to_dict()
                left_out.append(left_out_item)

        error = self.error

        catalog: str | Unset = UNSET
        if not isinstance(self.catalog, Unset):
            catalog = self.catalog.value

        catalog_version = self.catalog_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if body is not UNSET:
            field_dict["body"] = body
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if files is not UNSET:
            field_dict["files"] = files
        if left_out is not UNSET:
            field_dict["left_out"] = left_out
        if error is not UNSET:
            field_dict["error"] = error
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if catalog_version is not UNSET:
            field_dict["catalog_version"] = catalog_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.skill_request_left_out import SkillRequestLeftOut

        d = dict(src_dict)
        path = d.pop("path")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        body = d.pop("body", UNSET)

        sha256 = d.pop("sha256", UNSET)

        files = cast(list[str], d.pop("files", UNSET))

        _left_out = d.pop("left_out", UNSET)
        left_out: list[SkillRequestLeftOut] | Unset = UNSET
        if _left_out is not UNSET:
            left_out = []
            for left_out_item_data in _left_out:
                left_out_item = SkillRequestLeftOut.from_dict(left_out_item_data)

                left_out.append(left_out_item)

        error = d.pop("error", UNSET)

        _catalog = d.pop("catalog", UNSET)
        catalog: SkillRequestCandidateCatalog | Unset
        if isinstance(_catalog, Unset):
            catalog = UNSET
        else:
            catalog = SkillRequestCandidateCatalog(_catalog)

        catalog_version = d.pop("catalog_version", UNSET)

        skill_request_candidate = cls(
            path=path,
            name=name,
            description=description,
            body=body,
            sha256=sha256,
            files=files,
            left_out=left_out,
            error=error,
            catalog=catalog,
            catalog_version=catalog_version,
        )

        skill_request_candidate.additional_properties = d
        return skill_request_candidate

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
