from typing import Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from recipes.datatypes import RecipeType
from recipes.models import Recipe


class BaseCreateUpdateProtocol[T, M](Protocol):
    model: M

    async def add(self, session: AsyncSession, data: T) -> M: ...

    async def update(self, session: AsyncSession, pk: int | UUID, data: T) -> M: ...


class RecipeService(BaseCreateUpdateProtocol):
    model = Recipe

    async def add(self, session: AsyncSession, data: RecipeType) -> Recipe:
        recipe_obj = Recipe(**data.to_dict())
        session.add(recipe_obj)
        await session.commit()
        await session.refresh(recipe_obj)
        return recipe_obj

    async def update(self, session: AsyncSession, pk: UUID, data: RecipeType) -> Recipe:
        recipe_obj = await session.get(Recipe, pk)
        for key, value in data.to_dict().items():
            setattr(recipe_obj, key, value)
        await session.commit()
        await session.refresh(recipe_obj)
        return recipe_obj
