from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.domain.entities.user import User
from app.drivers.rest.dependencies import (
    get_create_user_use_case,
    get_enable_user_account_use_case,
)
from app.drivers.rest.routes.v1.schema import CreateUserInput
from app.use_cases.create_user_use_case import CreateUserUseCase
from app.use_cases.enable_user_account_use_case import EnableUserAccountUseCase


router = APIRouter()
security = HTTPBasic()


@router.post("/create", description="Create a new user")
async def create_user(
    create_user_use_case: Annotated[
        CreateUserUseCase, Depends(get_create_user_use_case)
    ],
    data: CreateUserInput = Body(...),
):
    await create_user_use_case(data.to_entity())
    return {"message": "Account created successfully"}


@router.post("/enable", description="enable user account")
async def enable_user(
    enable_user_account_use_case: Annotated[
        EnableUserAccountUseCase, Depends(get_enable_user_account_use_case)
    ],
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    code: Annotated[int, Query(description="4-digit activation code")],
):
    user = User(email=credentials.username, password=credentials.password)
    await enable_user_account_use_case(user, code)
    return {"message": "Account enabled successfully"}
