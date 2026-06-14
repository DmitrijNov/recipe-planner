from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class RecipeResponse(BaseModel):
    uuid: UUID
    title: str
    description: str
    image_url: str | None


class CreateRecipeSchema(BaseModel):
    title: Annotated[str, Field(max_length=25)]
    description: str
