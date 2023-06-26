import bpy
from .humanoid_properties import PROP_NAMES
from typing import Optional


def guess_bone(armature: bpy.types.Armature, prop: str) -> Optional[str]:
    tokens = prop.split("_")
    search = tokens[-1].lower()

    found = [bone.name for bone in armature.bones if search in bone.name.lower()]
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        if tokens[0] == "left":
            for f in found:
                if "left" in f.lower():
                    return f
        elif tokens[0] == "right":
            for f in found:
                if "right" in f.lower():
                    return f


class GuessHumanBones(bpy.types.Operator):
    bl_idname = "humanoid.guess_bones"
    bl_label = "Guess Humanoid Bones"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if context.active_object:
            return isinstance(context.active_object.data, bpy.types.Armature)
        return False

    def execute(self, context: bpy.types.Context):
        armature = context.active_object.data
        humanoid = armature.humanoid
        for prop in PROP_NAMES:
            bone = getattr(humanoid, prop)
            if not bone:
                bone = guess_bone(armature, prop)
                if bone:
                    setattr(humanoid, prop, bone)

        return {"FINISHED"}
