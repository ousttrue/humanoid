import contextlib
import struct
import bpy


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


def set_bone_group(obj: bpy.types.Object, bone_name: str, group_name: str, theme: str):
    group = get_or_create_bone_group(obj, group_name, theme)
    obj.pose.bones[bone_name].bone_group = group


def get_or_create_constraint(
    armature_obj: bpy.types.Object, pose_bone_name, constraint_type, constraint_name=""
):
    if not constraint_name:
        constraint_name = constraint_type
    if constraint_name in armature_obj.pose.bones[pose_bone_name].constraints:
        return armature_obj.pose.bones[pose_bone_name].constraints[constraint_name]
    armature_obj.data.bones.active = armature_obj.data.bones[pose_bone_name]
    bpy.ops.pose.constraint_add(type=constraint_type)
    return armature_obj.pose.bones[pose_bone_name].constraints[constraint_name]
