from . import types, ops, utils
from typing import List


class Objects:
    def new(self, name: str, data: types.Data) -> types.Object:
        ...

    def __iter__(self):
        ...

    def __getitem__(self, key) -> types.Object:
        ...


class data:
    objects: Objects
    armatures: types.Collection[types.Armature]


__all__ = ["types", "ops", "data", "utils"]
