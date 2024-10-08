from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from starlette import status

from app.models import CreateDemoScheme, DemoScheme
from app.services.demo import create_demo, get_demo_list

router = APIRouter()


@router.get("/demos", response_model=list[DemoScheme])
async def retrieve_demo_list() -> ORJSONResponse:
    return ORJSONResponse(jsonable_encoder(await get_demo_list()))


@router.post("/demos", response_model=DemoScheme, status_code=status.HTTP_201_CREATED)
async def create_one_demo(request: CreateDemoScheme) -> ORJSONResponse:
    return ORJSONResponse(
        jsonable_encoder(await create_demo(request)),
        status_code=status.HTTP_201_CREATED,
    )
