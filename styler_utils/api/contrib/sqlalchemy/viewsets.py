from re import L
from typing import Any

from fastapi import Request
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base

from styler_utils.api.viewsets import BaseGenericViewSet
from .mixins import *

class AlchemyGenericViewSet(BaseGenericViewSet):
    model: declarative_base()

    def __init__(self, request: Request, deps: Any = None, id: str = None, **kwargs):
        super().__init__(request, deps, id, **kwargs)
        self.session = self.context.session
    
    async def get_obj(self):
        smtp = select(self.model).filter_by(id=self.pk)
        return (await self.session.scalars(smtp)).first()

    def get_list_query(self):
        return select(self.model)


class ReadViewSet(ListMixin, AlchemyGenericViewSet):
    pass


class CreateViewSet(CreateMixin, AlchemyGenericViewSet):
    pass


class RetrieveViewSet(RetriveMixin, AlchemyGenericViewSet):
    pass


class DeleteViewSet(DeleteMixin, AlchemyGenericViewSet):
    pass


class UpdateViewSet(UpdateMixin, AlchemyGenericViewSet):
    pass


class ReadOnlyViewset(ListMixin, RetriveMixin, AlchemyGenericViewSet):
    pass


class ModelViewSet(
    ListMixin,
    CreateMixin,
    RetriveMixin,
    DeleteMixin,
    UpdateMixin,
    AlchemyGenericViewSet
):
    pass