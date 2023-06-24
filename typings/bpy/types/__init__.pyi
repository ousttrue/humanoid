import mathutils
from typing import Literal

class Armature:
    name: str
    show_names: bool
    show_axes: bool
    display_type: Literal["STICK", "OCTAHEDRAL"]

class EditBone:
    name: str
    head: mathutils.Vector
    tail: mathutils.Vector

class Operator:
    pass
