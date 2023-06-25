from typing import NamedTuple, Tuple, List, Optional
import bpy
import math


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

    # to object mode
    mode = context.object.mode
    if mode != "OBJECT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="OBJECT")

    # custom property
    armature.humanoid.hips = "Hips"
    armature.humanoid.spine = "Spine"
    armature.humanoid.chest = "Chest"
    armature.humanoid.neck = "Neck"
    armature.humanoid.head = "Head"

    armature.humanoid.left_shoulder = "Shoulder.L"
    armature.humanoid.left_upper_arm = "UpperArm.L"
    armature.humanoid.left_lower_arm = "LowerArm.L"
    armature.humanoid.left_hand = "Hand.L"
    armature.humanoid.right_shoulder = "Shoulder.R"
    armature.humanoid.right_upper_arm = "UpperArm.R"
    armature.humanoid.right_lower_arm = "LowerArm.R"
    armature.humanoid.right_hand = "Hand.R"

    armature.humanoid.left_upper_leg = "UpperLeg.L"
    armature.humanoid.left_lower_leg = "LowerLeg.L"
    armature.humanoid.left_foot = "Foot.L"
    armature.humanoid.left_toes = "Toes.L"
    armature.humanoid.right_upper_leg = "UpperLeg.R"
    armature.humanoid.right_lower_leg = "LowerLeg.R"
    armature.humanoid.right_foot = "Foot.R"
    armature.humanoid.right_toes = "Toes.R"


class CreateHumanoid(bpy.types.Operator):
    """CreateHumanoidArmature"""

    bl_idname = "humanoid.create"
    bl_label = "Create Humanoid Armature"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        create(context)
        return {"FINISHED"}
