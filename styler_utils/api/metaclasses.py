from abc import ABCMeta
from typing import Tuple, TypeVar

from pydantic import BaseModel

from .schemas import BaseMeta

MetaType = TypeVar("MetaType", bound=BaseModel)

def inherit_meta(meta: MetaType, parent_meta: MetaType) -> MetaType:
    if not meta:
        base_classes: Tuple[MetaType, ...] = (parent_meta,)
    elif meta == parent_meta:
        base_classes = (meta,)
    else:
        base_classes = meta, parent_meta
    return type("Meta", base_classes, {})


class BaseViewSetMetaclass(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        meta = namespace.get("Meta")
        new_name_space = {
            "meta": inherit_meta(meta, BaseMeta)(),
            **namespace
        }
        return super().__new__(mcs, name, bases, new_name_space, **kwargs)