import mathutils
from typing import Literal, Generic, TypeVar, Union, Tuple, Optional

T1 = TypeVar("T1")

class Collection(Generic[T1]):
    def new(self, name: str) -> T1: ...
    def __iter__(self): ...
    def __getitem__(self, key) -> T1: ...

class bpy_struct:
    name: str

class ID(bpy_struct):
    pass

class Bone(bpy_struct):
    pass

class EditBone(bpy_struct):
    #
    @property
    def head(self) -> mathutils.Vector: ...
    @head.setter
    def head(self, v: Union[mathutils.Vector, Tuple[float, float, float]]): ...

    #
    @property
    def tail(self) -> mathutils.Vector: ...
    @tail.setter
    def tail(self, v: Union[mathutils.Vector, Tuple[float, float, float]]): ...

    parent: Optional[EditBone]
    use_connect: bool

class PoseBone(bpy_struct):
    pass

class Armature(ID):
    show_names: bool
    show_axes: bool
    display_type: Literal["STICK", "OCTAHEDRAL"]
    edit_bones: Collection[EditBone]

class Object(bpy_struct):
    data: ID

class Panel(bpy_struct):
    pass

class Context(bpy_struct):
    """
    https://docs.blender.org/api/current/bpy.types.Context.html
    https://docs.blender.org/api/current/bpy.context.html#bpy.context.active_object
    """

    @property
    def active_object(self) -> Optional[Object]: ...
    @property
    def object(self) -> Optional[Object]: ...

class Operator:
    pass
