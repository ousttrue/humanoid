bl_info = {
    "name": "VrmHumanoid",
    "blender": (4, 1, 0),
    "category": "Rigging",
    "description": "Create vrm compliant humanoid armarture and copy humanoid pose to clipboard as UNIVRM_pose",
    "author": "ousttrue",
    "version": (3, 1, 0),
    "wiki_url": "https://github.com/ousttrue/humanoid",
}

import bpy
import importlib

if "humanoid_utils" in locals():
    importlib.reload(humanoid_utils)

if "humanoid_properties" in locals():
    importlib.reload(humanoid_properties)

if "create_humanoid" in locals():
    importlib.reload(create_humanoid)

if "add_humanoid_rig" in locals():
    importlib.reload(add_humanoid_rig)

if "copy_humanoid_pose" in locals():
    importlib.reload(copy_humanoid_pose)

if "guess_human_bones" in locals():
    importlib.reload(guess_human_bones)

if "humanoid_panel" in locals():
    importlib.reload(humanoid_panel)

from . import humanoid_utils
from .humanoid_properties import HumanoidProperties
from .create_humanoid import CreateHumanoid
from .add_humanoid_rig import AddHumanoidRig
from .copy_humanoid_pose import CopyHumanoidPose
from .guess_human_bones import GuessHumanBones
from .humanoid_panel import ArmatureHumanoidPanel, SelectPoseBone

OPERATORS = [
    CreateHumanoid,
    AddHumanoidRig,
    CopyHumanoidPose,
    GuessHumanBones,
    SelectPoseBone,
]
CLASSES = [HumanoidProperties, ArmatureHumanoidPanel] + OPERATORS


def add_to_menu(menu: str, op):
    def menu_func(self, context):
        if hasattr(op, "bl_icon"):
            self.layout.operator(op.bl_idname, icon=op.bl_icon)
        else:
            self.layout.operator(op.bl_idname)

    getattr(bpy.types, menu).prepend(menu_func)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

        if hasattr(cls, "bl_menu"):
            add_to_menu(cls.bl_menu, cls)

    bpy.types.Armature.humanoid = bpy.props.PointerProperty(type=HumanoidProperties)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
