from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db
from recipes.models import Recipe
from recipes.schemas import CreateRecipeSchema, RecipeResponse

router = APIRouter(prefix="/recipes")


@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(session: AsyncSession = Depends(db.session)):
    result = await session.scalars(select(Recipe))
    return result.all()


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe: CreateRecipeSchema, session: AsyncSession = Depends(db.session)
):
    new_recipe = Recipe(**recipe.model_dump(), image_url=None, author_id=8)
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe
