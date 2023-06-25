bl_info = {
    "name": "Humanoid",
    "blender": (3, 5, 0),
    "category": "Object",
    "description": "Create default amarture and copy pose to clipboard as VRM-animation",
    "author": "ousttrue",
    "version": (1, 0, 0),
}

if "bpy" in locals():
    import importlib

    if "humanoid_properties" in locals():
        importlib.reload(humanoid_properties)
    if "create_humanoid" in locals():
        importlib.reload(create_humanoid)
    if "copy_humanoid_pose" in locals():
        importlib.reload(copy_humanoid_pose)
    if "humanoid_panel" in locals():
        importlib.reload(humanoid_panel)


import bpy
from .humanoid_properties import HumanoidProperties
from .create_humanoid import CreateHumanoid
from .copy_humanoid_pose import CopyHumanoidPose
from .humanoid_panel import ArmatureHumanoidPanel


OPERATORS = [CreateHumanoid, CopyHumanoidPose]
CLASSES = [HumanoidProperties, ArmatureHumanoidPanel] + OPERATORS


def menu_func(self, context):
    for op in OPERATORS:
        self.layout.operator(op.bl_idname)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    bpy.types.Armature.humanoid = bpy.props.PointerProperty(type=HumanoidProperties)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
