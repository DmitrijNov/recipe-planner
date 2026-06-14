from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security.tokens import require_bearer_token
from core.database import db
from recipes.datatypes import RecipeType
from recipes.models import Recipe
from recipes.schemas import CreateRecipeSchema, RecipeResponse
from recipes.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipes", dependencies=[Depends(require_bearer_token)])


@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(session: AsyncSession = Depends(db.session)):
    result = await session.scalars(select(Recipe))
    return result.all()


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe_data: CreateRecipeSchema, session: AsyncSession = Depends(db.session)
):
    service = RecipeService()
    recipe_type = RecipeType(**recipe_data.model_dump(), author_id=8)
    obj = await service.add(data=recipe_type, session=session)

    return obj


@router.patch("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: str,
    data: CreateRecipeSchema,
    session: AsyncSession = Depends(db.session),
):
    recipe_type = RecipeType(**data.model_dump(), author_id=8)
    service = RecipeService()
    res = await service.update(session=session, pk=recipe_id, data=recipe_type)
    return res
