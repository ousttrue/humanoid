bl_info = {
    "name": "Humanoid",
    "blender": (3, 5, 0),
    "category": "Object",
}


import bpy
from enum import Enum
from typing import NamedTuple, List, Optional, Tuple
import mathutils


class HumanBones(Enum):
    hips = "hips"
    spine = "spine"
    chest = "chest"
    upperChest = "upperChest"
    neck = "neck"
    head = "head"
    leftEye = "leftEye"
    rightEye = "rightEye"
    jaw = "jaw"
    # arms
    leftShoulder = "Shoulder.L"
    leftUpperArm = "UpperArm.L"
    leftLowerArm = "LowerArm.L"
    leftHand = "Hand.L"
    rightShoulder = "Shoulder.R"
    rightUpperArm = "UpperArm.R"
    rightLowerArm = "LowerArm.R"
    rightHand = "Hand.R"
    # legs
    leftUpperLeg = "UpperLeg.L"
    leftLowerLeg = "LowerLeg.L"
    leftFoot = "Foot.L"
    leftToes = "Toes.L"
    rightUpperLeg = "UpperLeg.R"
    rightLowerLeg = "LowerLeg.R"
    rightFoot = "Foot.R"
    rightToes = "Toes.R"
    # fingers
    leftThumbMetacarpal = "ThumbMetacarpal.L"
    leftThumbProximal = "ThumbProximal.L"
    leftThumbDistal = "ThumbDistal.L"
    leftIndexProximal = "IndexProximal.L"
    leftIndexIntermediate = "IndexIntermediate.L"
    leftIndexDistal = "IndexDistal.L"
    leftMiddleProximal = "MiddleProximal.L"
    leftMiddleIntermediate = "MiddleIntermediate.L"
    leftMiddleDistal = "MiddleDistal.L"
    leftRingProximal = "RingProximal.L"
    leftRingIntermediate = "RingIntermediate.L"
    leftRingDistal = "RingDistal.L"
    leftLittleProximal = "LittleProximal.L"
    leftLittleIntermediate = "LittleIntermediate.L"
    leftLittleDistal = "LittleDistal.L"
    rightThumbMetacarpal = "ThumbMetacarpal.R"
    rightThumbProximal = "ThumbProximal.R"
    rightThumbDistal = "ThumbDistal.R"
    rightIndexProximal = "IndexProximal.R"
    rightIndexIntermediate = "IndexIntermediate.R"
    rightIndexDistal = "IndexDistal.R"
    rightMiddleProximal = "MiddleProximal.R"
    rightMiddleIntermediate = "MiddleIntermediate.R"
    rightMiddleDistal = "MiddleDistal.R"
    rightRingProximal = "RingProximal.R"
    rightRingIntermediate = "RingIntermediate.R"
    rightRingDistal = "RingDistal.R"
    rightLittleProximal = "LittleProximal.R"
    rightLittleIntermediate = "LittleIntermediate.R"
    rightLittleDistal = "LittleDistal.R"
    tip = "tip"


class Bone(NamedTuple):
    human_bone: HumanBones
    head: Tuple[float, float, float]
    children: List["Bone"] = []

    def create(
        self, armature: bpy.types.Armature, parent: Optional[bpy.types.EditBone] = None
    ):
        name = self.human_bone.name
        if parent and self.human_bone == HumanBones.tip:
            name = parent.name + ".tip"

        bone = get_or_create_bone(armature, name)
        bone.head = self.head
        if parent:
            bone.head += parent.head
        bone.tail = bone.head
        for i, child in enumerate(self.children):
            child_bone = child.create(armature, bone)
            if i == 0:
                bone.tail = child_bone.head
                child_bone.parent = bone
                child_bone.use_connect = True
        return bone


NECK_HEAD = Bone(
    HumanBones.neck,
    (0, 0, 1),
    [
        Bone(
            HumanBones.head,
            (0, 0, 1),
            [Bone(HumanBones.tip, (0, 0, 1))],
        )
    ],
)

LEFT_ARM = Bone(
    HumanBones.leftShoulder,
    (1, 0, 1),
    [
        Bone(
            HumanBones.leftUpperArm,
            (1, 0, 0),
            [
                Bone(
                    HumanBones.leftLowerArm,
                    (1, 0, 0),
                    [
                        Bone(
                            HumanBones.leftHand,
                            (1, 0, 0),
                            [Bone(HumanBones.tip, (1, 0, 0))],
                        )
                    ],
                )
            ],
        )
    ],
)
RIGHT_ARM = Bone(
    HumanBones.rightShoulder,
    (-1, 0, 1),
    [
        Bone(
            HumanBones.rightUpperArm,
            (-1, 0, 0),
            [
                Bone(
                    HumanBones.rightLowerArm,
                    (-1, 0, 0),
                    [
                        Bone(
                            HumanBones.rightHand,
                            (-1, 0, 0),
                            [Bone(HumanBones.tip, (-1, 0, 0))],
                        )
                    ],
                )
            ],
        )
    ],
)

LEFT_LEG = Bone(
    HumanBones.leftUpperLeg,
    (1, 0, 0),
    [
        Bone(
            HumanBones.leftLowerLeg,
            (0, 0, -1),
            [
                Bone(
                    HumanBones.leftFoot,
                    (0, 0, -1),
                    [
                        Bone(
                            HumanBones.leftToes,
                            (0, -1, -1),
                            [Bone(HumanBones.tip, (0, -1, 0))],
                        )
                    ],
                )
            ],
        ),
    ],
)

RIGHT_LEG = Bone(
    HumanBones.rightUpperLeg,
    (-1, 0, 0),
    [
        Bone(
            HumanBones.rightLowerLeg,
            (0, 0, -1),
            [
                Bone(
                    HumanBones.rightFoot,
                    (0, 0, -1),
                    [
                        Bone(
                            HumanBones.rightToes,
                            (0, -1, -1),
                            [Bone(HumanBones.tip, (0, -1, 0))],
                        )
                    ],
                )
            ],
        ),
    ],
)

HUMANOID = Bone(
    HumanBones.hips,
    (0, 0, 1),
    [
        Bone(
            HumanBones.spine,
            (0, 0, 1),
            [
                Bone(
                    HumanBones.chest,
                    (0, 0, 1),
                    [
                        NECK_HEAD,
                        LEFT_ARM,
                        RIGHT_ARM,
                    ],
                )
            ],
        ),
        LEFT_LEG,
        RIGHT_LEG,
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

    armature.show_names = True
    armature.show_axes = True
    armature.use_mirror_x = True
    armature.display_type = "OCTAHEDRAL"

    HUMANOID.create(armature)


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
