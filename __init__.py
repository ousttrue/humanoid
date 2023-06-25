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


class HumanoidProperties(bpy.types.PropertyGroup):
    hips: bpy.props.StringProperty(name="hips")
    spine: bpy.props.StringProperty(name="spine")
    chest: bpy.props.StringProperty(name="chest")
    neck: bpy.props.StringProperty(name="neck")
    head: bpy.props.StringProperty(name="head")
    #
    left_shoulder: bpy.props.StringProperty(name="left_shoulder")
    left_upper_arm: bpy.props.StringProperty(name="left_upper_arm")
    left_lower_arm: bpy.props.StringProperty(name="left_lower_arm")
    left_hand: bpy.props.StringProperty(name="left_hand")
    right_shoulder: bpy.props.StringProperty(name="right_shoulder")
    right_upper_arm: bpy.props.StringProperty(name="right_upper_arm")
    right_lower_arm: bpy.props.StringProperty(name="right_lower_arm")
    right_hand: bpy.props.StringProperty(name="right_hand")
    #
    left_upper_leg: bpy.props.StringProperty(name="left_upper_leg")
    left_lower_leg: bpy.props.StringProperty(name="left_lower_leg")
    left_foot: bpy.props.StringProperty(name="left_foot")
    left_toes: bpy.props.StringProperty(name="left_toes")
    right_upper_leg: bpy.props.StringProperty(name="right_upper_leg")
    right_lower_leg: bpy.props.StringProperty(name="right_lower_leg")
    right_foot: bpy.props.StringProperty(name="right_foot")
    right_toes: bpy.props.StringProperty(name="right_toes")


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


class ArmatureHumanoidPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_humanoid"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Humanoid"
    bl_label = "Humanoid"

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return isinstance(context.active_object.data, bpy.types.Armature)

    def draw_bone(self, armature: bpy.types.Armature, bone: str):
        self.layout.prop_search(armature.humanoid, bone, armature, "bones")

    def draw_bone_lr(self, armature: bpy.types.Armature, bone: str):
        split = self.layout.split(factor=0.24)
        split.label(text=f"{bone}:")
        split.column().prop_search(
            armature.humanoid, f"left_{bone}", armature, "bones", text=""
        )
        split.column().prop_search(
            armature.humanoid, f"right_{bone}", armature, "bones", text=""
        )

    def draw(self, context):
        armature = context.active_object.data
        self.draw_bone(armature, "hips")
        self.draw_bone(armature, "spine")
        self.draw_bone(armature, "chest")
        self.draw_bone(armature, "neck")
        self.draw_bone(armature, "head")
        self.draw_bone_lr(armature, "shoulder")
        self.draw_bone_lr(armature, "upper_arm")
        self.draw_bone_lr(armature, "lower_arm")
        self.draw_bone_lr(armature, "hand")
        self.draw_bone_lr(armature, "upper_leg")
        self.draw_bone_lr(armature, "lower_leg")
        self.draw_bone_lr(armature, "foot")
        self.draw_bone_lr(armature, "toes")


CLASSES = [CreateHumanoid, HumanoidProperties, ArmatureHumanoidPanel]


def menu_func(self, context):
    self.layout.operator(CreateHumanoid.bl_idname)


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
