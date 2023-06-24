bl_info = {
    "name": "Humanoid",
    "blender": (3, 5, 0),
    "category": "Object",
}


import bpy
import math
from typing import NamedTuple, List, Optional, Tuple
import mathutils


class Bone(NamedTuple):
    human_bone: str
    head: Tuple[float, float, float]
    children: List["Bone"] = []

    def create(
        self, armature: bpy.types.Armature, parent: Optional[bpy.types.EditBone] = None
    ):
        name = self.human_bone
        if parent and self.human_bone == "tip":
            name = parent.name + ".tip"

        bone = get_or_create_bone(armature, name)
        bone.head = self.head
        if parent:
            bone.head += parent.head
        if bone.head.x > 0:
            bone.name += ".L"
        elif bone.head.x < 0:
            bone.name += ".R"
        bone.tail = bone.head
        for i, child in enumerate(self.children):
            child_bone = child.create(armature, bone)
            if i == 0:
                bone.tail = child_bone.head
                child_bone.parent = bone
                child_bone.use_connect = True
        return bone


def get_arm(lr: float):
    return Bone(
        "Shoulder",
        (lr * 0.1, 0, math.fabs(lr) * 2),
        [
            Bone(
                "UpperArm",
                (lr, 0, 0),
                [
                    Bone(
                        "LowerArm",
                        (lr * 2, 0, 0),
                        [
                            Bone(
                                "Hand",
                                (lr * 2, 0, 0),
                                [Bone("tip", (lr, 0, 0))],
                            )
                        ],
                    )
                ],
            )
        ],
    )


def get_leg(tall: float, lr: float):
    # upper 1
    # lower 1
    # foot 0.2
    base = tall / 11
    return Bone(
        "UpperLeg",
        (lr * base, 0, 0),
        [
            Bone(
                "LowerLeg",
                (0, 0, -base * 5),
                [
                    Bone(
                        "Foot",
                        (0, 0, -base * 5),
                        [
                            Bone(
                                "Toes",
                                (0, -base, -base),
                                [Bone("tip", (0, -base, 0))],
                            )
                        ],
                    )
                ],
            ),
        ],
    )


def get_humanoid(tall: float):
    head = tall / 6
    # head=1
    #
    # neck  1
    # chest 4
    # spine 2
    # hips  2
    base = head * 2 / 9
    return Bone(
        "Hips",
        (0, 0, tall / 2),
        [
            Bone(
                "Spine",
                (0, 0, base * 2),
                [
                    Bone(
                        "Chest",
                        (0, 0, base * 2),
                        [
                            Bone(
                                "Neck",
                                (0, 0, base * 4),
                                [
                                    Bone(
                                        "Head",
                                        (0, 0, base),
                                        [Bone("tip", (0, 0, head))],
                                    )
                                ],
                            ),
                            get_arm(base * 2),
                            get_arm(-base * 2),
                        ],
                    )
                ],
            ),
            get_leg(tall / 2, 1),
            get_leg(tall / 2, -1),
        ],
    )


def activate(context, obj):
    context.view_layer.objects.active = obj
    obj.select_set(True)


def get_or_create_bone(armature: bpy.types.Armature, name: str):
    if name in armature.edit_bones:
        return armature.edit_bones[name]
    return armature.edit_bones.new(name)


def create(context):
    armature: bpy.types.Armature = bpy.data.armatures.new("Humanoid")
    obj = bpy.data.objects.new("Humanoid", armature)
    context.scene.collection.objects.link(obj)

    activate(context, obj)

    # to edit mode
    mode = context.object.mode
    if mode != "EDIT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="EDIT")

    # armature.show_names = True
    armature.show_axes = True
    armature.use_mirror_x = True
    armature.display_type = "OCTAHEDRAL"

    humanoid = get_humanoid(1.6)

    humanoid.create(armature)


class CreateHumanoid(bpy.types.Operator):
    """CreateHumanoidArmature"""

    bl_idname = "object.create_humanoid"
    bl_label = "Create Humanoid Armature"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        create(context)
        return {"FINISHED"}


CLASSES = [CreateHumanoid]


def menu_func(self, context):
    for cls in CLASSES:
        self.layout.operator(cls.bl_idname)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
