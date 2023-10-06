from fastapi import Request
from typing import TypeVar, Union


from pydantic import BaseModel

from .metaclasses import BaseViewSetMetaclass
from .helpers import ViewSetHelper


Dependencies = TypeVar("Dependencies")
HelperType  = TypeVar("HelperType", bound=ViewSetHelper)

class BaseGenericViewSet(metaclass=BaseViewSetMetaclass):
    dependencies: dict | Dependencies = {}
    pagination: HelperType = None
    filters: list[HelperType] = []
    permissions: list[HelperType] = []
    helpers: list[HelperType] = []    

    request: Request
    context: BaseModel

    def __init__(
        self,
        request: Request,
        deps: Dependencies = None,
        id: Union[int, str] = None,
        pagination: HelperType = None,
        filters: list[HelperType] = [],
        helpers: list[HelperType] = [],
        **kwargs
    ):
        self.request = request
        self.deps = deps
        self.pk = id
        self.context = request.state.context
        self.pagination = pagination
        self.filters = filters
        self.helpers = helpers
    
    async def get_obj(self):
        raise NotImplementedError("Model was not specified")

    async def get_queryset(self):
        raise NotImplementedError("Model was not specified")