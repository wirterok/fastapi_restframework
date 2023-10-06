from collections import namedtuple
from functools import cached_property
from gc import callbacks
import inspect
from pydoc import Helper, resolve
from typing import Type, Any, TypeVar, get_type_hints, Callable, Awaitable, Generator, Union, OrderedDict

from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute, Request

from .helpers import DependencyHelper, ViewSetHelper
from .viewsets import BaseGenericViewSet
from .schemas import BaseRouteConfig

ViewSetType = TypeVar("ViewSetType", bound=BaseGenericViewSet)


class ResolverCallback:
    func: Union[Callable, Awaitable]
    allowed_fields: list

    def __init__(
        self, 
        func,
        ignore_signature_fields=('self', 'args', 'kwargs')
    ) -> None:
        self.ignore_signature_fields = ignore_signature_fields
        self.func = func

    @cached_property
    def route_config(self) -> dict:
        return getattr(self.func, "config", BaseRouteConfig()).dict()
    
    @cached_property
    def signature(self) -> inspect.Signature:
        sig = inspect.Signature.from_callable(self.func, follow_wrapped=True)

        return sig.replace(
            parameters=[v for k,v in sig.parameters.items() if k not in self.ignore_signature_fields]
        )
    
    @cached_property
    def parameters(self) -> OrderedDict:
        return dict(self.signature.parameters).values()

    @cached_property
    def name(self):
        return self.func.__name__

    def filter_dict_params(self, params: dict) -> dict:
        allowed_params = dict(self.signature.parameters).items()
        return {k:v for k,v in params.items() if k in allowed_params}


class ViewsetHelpersResolver:
    
    def __init__(self, viewset: ViewSetType) -> None:
        self.viewset = viewset

    def helper_list_to_dependency(self, name: str, helpers: list[ViewSetHelper]) -> Callable:
        def inner(**kwargs) -> dict:
            return kwargs
        parameters = [helper(self.viewset).dependency_param for helper in helpers]
        inner.__signature__ = inspect.Signature(
            parameters=parameters,
            return_annotation=dict
        )
        return inspect.Parameter(
            name=name,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default = Depends(inner),
            annotation=dict
        )

    @property
    def dependency_params(self) -> list[inspect.Parameter]:
        dependencies = []
        if self.viewset.dependencies:
            dependencies.append(DependencyHelper(self.viewset).dependency_param)
        if permissions := self.viewset.permissions:
            dependencies.append(self.helper_list_to_dependency("permissions", permissions))
        if filters := self.viewset.filters:
            dependencies.append(self.helper_list_to_dependency("filters", filters))
        if helpers := self.viewset.helpers:
            dependencies.append(self.helper_list_to_dependency("helpers", helpers))
        return dependencies


class Resolver:
    viewset: ViewSetType
    actions: dict[str, str]

    def __init__(
        self, 
        viewset: BaseGenericViewSet, 
        actions: dict = {}, 
        prefix: str = "", 
        detail: bool = False
    ) -> None:
        self.viewset = viewset
        self.actions = actions
        self.prefix = prefix + '/{id}' if detail else prefix
        self.detail = detail
        self.helpers_resolver = ViewsetHelpersResolver(viewset)

    @cached_property
    def required_parameters(self) -> list[inspect.Parameter]:
        params = [
            inspect.Parameter(
                name="request",
                kind=inspect.Parameter.POSITIONAL_ONLY,
                annotation=Request
            ), 
        ]
        if self.detail:
            params.append(
                inspect.Parameter(
                    name="id",
                    kind=inspect.Parameter.POSITIONAL_ONLY,
                    annotation=Union[int, str]
                )
            )
        return params

    @cached_property
    def positional_parameters(self) -> list[inspect.Parameter]:
        return self.helpers_resolver.dependency_params
    
    def get_prefix(self, callback):
        return self.prefix

    def filtered_http_viewset(self) -> Generator:
        # This method can be redefined in children classes
        viewset_members = dict(inspect.getmembers(self.viewset))
        reversed_actions = {v:k for k,v in self.actions.items()}
        for method, http_method in reversed_actions.items():
            if not (callback := viewset_members.get(method)):
                continue
            yield {"methods": [http_method.upper()]}, callback

    def generate_callback(self, resolver_callback: ResolverCallback) -> Callable[..., Any]:
        async def inner(*args, **kwargs):
            viewset = self.viewset(*args, **kwargs)
            executor = getattr(viewset, resolver_callback.name)
            if not viewset.meta.allow_extra_kwargs:
                kwargs = resolver_callback.filter_dict_params(kwargs)
            if inspect.iscoroutinefunction(executor):
                return await executor(**kwargs)
            else:
                return executor(**kwargs)

        inner.__name__ = resolver_callback.name
        inner.__signature__ = inspect.Signature(
            [
                *self.required_parameters,
                *resolver_callback.parameters, 
                *self.positional_parameters
            ]
        )
        return inner
        
    def add_routes(self, router: APIRouter) -> None:
        for settings, viewset_method in self.filtered_http_viewset():
            resolver_callback = ResolverCallback(viewset_method)
            router.add_api_route(
                self.get_prefix(resolver_callback),
                self.generate_callback(resolver_callback),
                **settings,
                **resolver_callback.route_config,
            )


class ActionResolver(Resolver):

    def get_prefix(self, callback: ResolverCallback):
        return super().get_prefix(callback) + callback.name

    def filtered_http_viewset(self) -> Generator:
        # This method can be redefined in children classes
        for name, func in inspect.getmembers(self.viewset):
            if not getattr(func, "is_action", False) or self.detail != getattr(func, "detail", False):
                continue
            yield {"methods": [func.methods]}, func
