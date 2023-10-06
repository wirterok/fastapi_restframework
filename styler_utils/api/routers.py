from typing import List

from fastapi import APIRouter

from .viewsets import BaseGenericViewSet

from .resolvers import Resolver, ActionResolver
from .constants import DEFAULT_ACTIONS, DEFAULT_DETAIL_ACTIONS

class ViewsetRouter(APIRouter):
    
    def include_viewset(self, viewset: BaseGenericViewSet, resolvers: List[Resolver] = []):
        resolvers.extend([
            Resolver(
                viewset=viewset,
                prefix=self.prefix,
                actions=DEFAULT_DETAIL_ACTIONS,
                detail=True
            ),
            Resolver(
                viewset=viewset,
                prefix=self.prefix,
                actions=DEFAULT_ACTIONS
            ),
            # ActionResolver(
            #     viewset=viewset,
            #     prefix=self.prefix
            # ),
            
            # ActionResolver(
            #     viewset=viewset,
            #     prefix=self.prefix,
            #     detail=True
            # )
        ])
        for resolver in resolvers:
            resolver.add_routes(self)
