from functools import cached_property
import inspect
from collections import namedtuple
from typing import Any, get_type_hints

from fastapi import Depends
from sqlalchemy.sql import Select


class ViewSetHelper:
    # __slots__ are required for fastapi schema generation

    def __init__(self, viewset) -> None:
        self.viewset = viewset

    @property
    def dependency_param(self) -> inspect.Parameter:
        raise NotImplementedError("Dependency was not defined")

    @property
    def instantiator(self):
        def inner(**kwargs):
            return self.__class__(self.viewset, **kwargs)
        return inner

    @cached_property
    def dependency_param(self):
        if not getattr(self, "__slots__", None):
            return

        callback = self.instantiator
        deps_params = [
            inspect.Parameter(
                name=value,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=type(getattr(self.__class__, value, None)),
                annotation=int
            )
            for value in self.__slots__
        ]
        callback.__signature__ = inspect.Signature(deps_params)
        return inspect.Parameter(
            name=self.__name__,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default = Depends(callback),
            annotation=self.__class__
        )
        

class BaseCustomViewsetHelper(ViewSetHelper):

    def modify_query(self) -> Select:
        raise NotImplementedError("Helper logic vas not defined")


class BaseFilterViewsetHelper(ViewSetHelper):

    def filter_query(self) -> Select:
        raise NotImplementedError("Filtered logic was not implemented")


class DependencyHelper(ViewSetHelper):
    
    @cached_property
    def dependency_param(self):
        Dependencies = namedtuple("Dependencies", self.viewset.dependencies.keys())
        def dependencies(**kwargs):
            return Dependencies(**kwargs)
        deps_params = [
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Depends(callback),
                annotation=get_type_hints(callback).get("return", Any)
            )
            for name,callback in self.viewset.dependencies.items()
        ]
        dependencies.__signature__ = inspect.Signature(deps_params, return_annotation=Dependencies)
        return inspect.Parameter(
            name="dependencies",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default = Depends(dependencies),
            annotation=Dependencies
        )


class PaginationHelper(ViewSetHelper):
    __slots__ = "page_size", "page"

    # page_size: int = 100
    # page: int = 1


    def __init__(self, viewset, page_size: int = 100, page: int = 1) -> None:
        super().__init__(viewset)
        self.page = page
        self.page_size = page_size

    def paginate(self) -> Select:
        raise NotImplementedError("Pagination logic vas not implemented")


class OrderingHelper(BaseFilterViewsetHelper):
    ordering: str

    __slots__ = "ordering",

    def __init__(self, viewset, ordering: str = None) -> None:
        super().__init__(viewset)
        self.ordering = ordering


class SearchHelper(BaseFilterViewsetHelper):
    search: str

    __slots__ = "search"

    def __init__(self, viewset, search: str = None) -> None:
        super().__init__(viewset)
        self.search = search
