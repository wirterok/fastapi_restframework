from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import JSONResponse, Response
from fastapi.datastructures import Default
from fastapi.routing import BaseRoute, APIRoute
from starlette.types import ASGIApp
from fastapi.utils import generate_unique_id

from typing import Optional, List, Union, Sequence, Type, Dict, Callable, Any
from enum import Enum

from .schemas import RouteConfig

def extra(
    response_model: Any = None,
    status_code: Optional[int] = None,
    tags: Optional[List[Union[str, Enum]]] = None,
    dependencies: Optional[Sequence[Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[Any, Any]] = None,
    response_model_exclude: Optional[Union[Any, Any]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Type[Response] = Default(JSONResponse),
    name: Optional[str] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Callable[[APIRoute], str] = Default(
        generate_unique_id
    ),
):
    def inner(func):
        func.config = RouteConfig(
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )
        return func
    return inner


def action(
    methods: list,
    *,
    detail: bool = False,
    response_model: Any = None,
    status_code: Optional[int] = None,
    tags: Optional[List[Union[str, Enum]]] = None,
    dependencies: Optional[Sequence[Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[Any, Any]] = None,
    response_model_exclude: Optional[Union[Any, Any]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Type[Response] = Default(JSONResponse),
    name: Optional[str] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    generate_unique_id_function: Callable[[APIRoute], str] = Default(
        generate_unique_id
    ),
):
    def inner(func):
        func.config = RouteConfig(
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )
        func.methods = methods
        func.detail = detail
        return func
    return inner