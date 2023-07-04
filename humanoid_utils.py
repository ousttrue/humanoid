import contextlib
import struct
import bpy
from typing import Optional


def prop_to_name(armature: bpy.types.Armature, prop) -> Optional[str]:
    if hasattr(armature.humanoid, prop):
        return getattr(armature.humanoid, prop)


def get_human_bone(armature: bpy.types.Armature, prop):
    name = prop_to_name(armature, prop)
    if name:
        return armature.bones[name]
    else:
        return armature.bones[prop]


def get_human_editbone(armature: bpy.types.Armature, prop):
    name = prop_to_name(armature, prop)
    if name:
        return armature.edit_bones[name]
    else:
        return armature.edit_bones[prop]


def get_human_posebone(obj: bpy.types.Object, prop):
    name = prop_to_name(obj.data, prop)
    if name:
        return obj.pose.bones[name]
    else:
        return obj.pose.bones[prop]


def get_or_create_editbone(armature: bpy.types.Armature, name: str):
    if name in armature.edit_bones:
        return armature.edit_bones[name]
    return armature.edit_bones.new(name)


@contextlib.contextmanager
def enter_pose(obj: bpy.types.Object):
    bpy.context.view_layer.objects.active = obj
    if bpy.context.mode == "POSE":
        yield
    else:
        bpy.ops.object.posemode_toggle()
        try:
            yield
        finally:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.posemode_toggle()


def get_or_create_bone_group(
    armature_obj: bpy.types.Object, name: str, theme: str
) -> bpy.types.BoneGroup:
    if name not in armature_obj.pose.bone_groups:
        group = armature_obj.pose.bone_groups.new(name=name)
        group.color_set = theme  # "THEME05"
    return armature_obj.pose.bone_groups[name]


def set_bone_group(obj: bpy.types.Object, prop: str, group_name: str, theme: str):
    group = get_or_create_bone_group(obj, group_name, theme)
    pose_bone = get_human_posebone(obj, prop)
    pose_bone.bone_group = group


def get_or_create_constraint(
    armature_obj: bpy.types.Object, pose_bone_name, constraint_type, constraint_name=""
):
    if not constraint_name:
        constraint_name = constraint_type
    if constraint_name in get_human_posebone(armature_obj, pose_bone_name).constraints:
        return get_human_posebone(armature_obj, pose_bone_name).constraints[
            constraint_name
        ]
    armature_obj.data.bones.active = get_human_bone(armature_obj.data, pose_bone_name)
    bpy.ops.pose.constraint_add(type=constraint_type)
    return get_human_posebone(armature_obj, pose_bone_name).constraints[constraint_name]
