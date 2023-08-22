from typing import List

from pydantic import BaseModel, Field, computed_field

class EntityName(BaseModel):
    domain: str = Field(repr=False)
    kind: str = Field(repr=False)

    @computed_field
    def entity_id_prefix(self) -> str:
        """following my hass entity_id naming standards
        """
        return f"{self.domain}.{self.kind}_"

    def is_match(self, entity_id: str) -> bool:
        entity_name = entity_id.removeprefix(f"{self.domain}.")
        return entity_name.startswith(f"{self.kind}.")


class EntityNames(BaseModel):
    entity_names: List[EntityName] = []
