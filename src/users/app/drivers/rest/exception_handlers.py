"""
THis file contains exception handlers for Fastapi drivers
"""

import json
import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.adapters.exceptions import ExternalError
from app.shared.logging import get_json_logger
from app.use_cases.exceptions import (
    IncorrectActivationCodeError,
    InvalidEmailFormatError,
    InvalidPasswordError,
    UserEmailAlreadyExistsError,
    UserInfoDoesntMatchError,
)


logging.basicConfig(level=logging.INFO)
logger = get_json_logger(__name__, log_lvl=logging.ERROR)


async def get_body(request: Request):
    try:
        body = await request.body()
    except Exception:
        return "Unable to retrieve body"

    try:
        json_body = json.loads(body)
    except Exception:
        try:
            json_body = body.decode()
        except Exception:
            return "Body is not JSON or text"

    return json_body


def exception_container(app: FastAPI) -> None:

    @app.exception_handler(InvalidEmailFormatError)
    async def invalid_email_format_exception_handler(
        request: Request, exc: InvalidEmailFormatError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidPasswordError)
    async def invalid_password_exception_handler(
        request: Request, exc: InvalidPasswordError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserEmailAlreadyExistsError)
    async def user_email_already_exist_exception_handler(
        request: Request, exc: UserEmailAlreadyExistsError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"message": str(exc)},
        )

    @app.exception_handler(IncorrectActivationCodeError)
    async def incorrect_activation_code_exception_handler(
        request: Request, exc: IncorrectActivationCodeError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(UserInfoDoesntMatchError)
    async def user_info_doesnt_match_exception_handler(
        request: Request, exc: UserInfoDoesntMatchError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(ExternalError)
    async def external_exception_handler(
        request: Request, exc: ExternalError
    ) -> JSONResponse:
        body = await get_body(request)
        url = str(request.url)
        error_message = {"url": url, "body": body, "message": exc}
        logger.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something went wrong. Please try again"},
        )
