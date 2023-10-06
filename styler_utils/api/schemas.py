from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import JSONResponse, Response
from fastapi.datastructures import Default
from fastapi.routing import BaseRoute, APIRoute
from starlette.types import ASGIApp
from fastapi.utils import generate_unique_id

from typing import Optional, List, Union, Sequence, Type, Dict, Callable, Any
from enum import Enum

from pydantic import BaseModel

class BaseRouteConfig(BaseModel):
    response_model: Any = None
    status_code: Optional[int] = None
    tags: Optional[List[Union[str, Enum]]] = None
    dependencies: Optional[Sequence[Depends]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    response_description: str = "Successful Response"
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    deprecated: Optional[bool] = None
    operation_id: Optional[str] = None
    response_model_include: Optional[Union[Any, Any]] = None
    response_model_exclude: Optional[Union[Any, Any]] = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: Type[Response] = Default(JSONResponse)
    name: Optional[str] = None
    callbacks: Optional[List[BaseRoute]] = None
    openapi_extra: Optional[Dict[str, Any]] = None
    generate_unique_id_function: Callable[[APIRoute], str] = Default(
        generate_unique_id
    )

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class BaseMeta(BaseModel):
    allow_extra_kwargs: bool = False

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
