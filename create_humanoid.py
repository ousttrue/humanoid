from typing import NamedTuple, Tuple, List, Optional, cast
import bpy
import math
from mathutils import Vector
from .enter_pose_mode import enter_pose

ROLL_MAP = {
    "Shoulder.L": 90,
    "UpperArm.L": 90,
    "LowerArm.L": 90,
    "Shoulder.R": -90,
    "UpperArm.R": -90,
    "LowerArm.R": -90,
    "Toes.L": 180,
    "Toes.R": 180,
    "ThumbMetacarpal.L": -90,
    "ThumbProximal.L": -90,
    "ThumbDistal.L": -90,
    "ThumbMetacarpal.R": 90,
    "ThumbProximal.R": 90,
    "ThumbDistal.R": 90,
    "IndexProximal.L": 180,
    "IndexIntermediate.L": 180,
    "IndexDistal.L": 180,
    "MiddleProximal.L": 180,
    "MiddleIntermediate.L": 180,
    "MiddleDistal.L": 180,
    "RingProximal.L": 180,
    "RingIntermediate.L": 180,
    "RingDistal.L": 180,
    "LittleProximal.L": 180,
    "LittleIntermediate.L": 180,
    "LittleDistal.L": 180,
    "IndexProximal.R": 180,
    "IndexIntermediate.R": 180,
    "IndexDistal.R": 180,
    "MiddleProximal.R": 180,
    "MiddleIntermediate.R": 180,
    "MiddleDistal.R": 180,
    "RingProximal.R": 180,
    "RingIntermediate.R": 180,
    "RingDistal.R": 180,
    "LittleProximal.R": 180,
    "LittleIntermediate.R": 180,
    "LittleDistal.R": 180,
}


class Bone(NamedTuple):
    human_bone: str
    head: Tuple[float, float, float]
    children: List["Bone"] = []

    def create(self, armature: bpy.types.Armature, parent: bpy.types.EditBone):
        name = self.human_bone
        if parent and self.human_bone == "tip":
            name = parent.name + ".tip"

        bone = get_or_create_bone(armature, name)
        bone.head = self.head
        if parent:
            bone.parent = parent
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
                child_bone.use_connect = True
        return bone


def get_finger(name: str, lr: float, y: float) -> Bone:
    """
    手首から指: 10
    指: 5-3-2
    親指: 5-4-3
    """
    base = lr / 10
    return Bone(
        f"{name}Proximal",
        (base * 10, y, 0),
        [
            Bone(
                f"{name}Intermediate",
                (base * 5, 0, 0),
                [
                    Bone(
                        f"{name}Distal",
                        (base * 3, 0, 0),
                        [Bone("tip", (base * 2, 0, 0))],
                    )
                ],
            )
        ],
    )


def get_thumb(x: float, y: float, z: float) -> Bone:
    base = x / 10
    return Bone(
        f"ThumbMetacarpal",
        (base * 3, y, z),
        [
            Bone(
                f"ThumbProximal",
                (base * 5, 0, 0),
                [
                    Bone(
                        f"ThumbDistal",
                        (base * 3, 0, 0),
                        [Bone("tip", (base * 2, 0, 0))],
                    )
                ],
            )
        ],
    )


def get_arm(lr: float) -> Bone:
    f = lr * 0.6
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
                                [
                                    get_finger("Middle", f, 0),
                                    get_finger("Index", f, -0.02),
                                    get_finger("Ring", f * 0.9, 0.02),
                                    get_finger("Little", f * 0.8, 0.03),
                                    get_thumb(f, -0.03, -0.02),
                                ],
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


def make_inverted_pelvis(obj: bpy.types.Object):
    mode = bpy.context.object.mode
    if mode != "EDIT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="EDIT")

    armature = cast(bpy.types.Armature, obj.data)

    cog = armature.edit_bones.new("COG")
    cog.parent = armature.edit_bones["root"]
    cog.head = armature.edit_bones["Spine"].head
    cog.tail = (cog.head.x, cog.head.y + 0.4, cog.head.z)

    pelvis = armature.edit_bones.new("Pelvis")
    pelvis.parent = cog
    pelvis.use_connect = False
    pelvis.head = cog.head
    pelvis.tail = armature.edit_bones["Hips"].head

    armature.edit_bones["Hips"].parent = pelvis
    with enter_pose(obj):
        hips = obj.pose.bones["Hips"]
        hips.lock_rotation = (True, True, True)
        hips.lock_scale = (True, True, True)
        armature.bones["Hips"].hide = True

    armature.bones["Spine"].use_inherit_rotation = False


def make_leg_ik(obj: bpy.types.Object, suffix: str):
    mode = bpy.context.object.mode
    if mode != "EDIT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="EDIT")

    armature = cast(bpy.types.Armature, obj.data)

    foot_name = f"Foot{suffix}"
    foot_offset_name = f"FootOffset{suffix}"
    ik_name = f"LegIK{suffix}"
    lower_name = f"LowerLeg{suffix}"
    pole_name = f"LegPole{suffix}"

    ik_head = armature.edit_bones[foot_name].head
    ik = armature.edit_bones.new(ik_name)
    ik.parent = armature.edit_bones["root"]
    ik.use_connect = False
    ik.head = ik_head
    ik.tail = (ik_head.x, ik_head.y + 0.2, ik_head.z)

    pole_head = armature.edit_bones[lower_name].head
    pole = armature.edit_bones.new(pole_name)
    pole.parent = ik
    pole.use_connect = False
    pole.head = (pole_head.x, pole_head.y - 0.4, pole_head.z)
    pole.tail = (pole_head.x, pole_head.y - 0.6, pole_head.z)

    lower = armature.edit_bones[lower_name]
    lower.head = (lower.head.x, lower.head.y - 0.01, lower.head.z)

    foot_offset = armature.edit_bones.new(foot_offset_name)
    foot_offset.parent = ik
    foot_offset.use_connect = False
    foot_offset.head = armature.edit_bones[foot_name].head
    foot_offset.tail = armature.edit_bones[foot_name].tail

    with enter_pose(obj):
        # IK
        armature.bones.active = armature.bones[lower_name]
        bpy.ops.pose.constraint_add(type="IK")
        c = obj.pose.bones[lower_name].constraints["IK"]
        c.target = obj
        c.subtarget = ik_name
        c.pole_target = obj
        c.pole_subtarget = pole_name
        c.pole_angle = math.pi * (-90) / 180
        c.chain_count = 2
        # FootCopy
        armature.bones.active = armature.bones[foot_name]
        bpy.ops.pose.constraint_add(type="COPY_ROTATION")
        c = obj.pose.bones[foot_name].constraints["Copy Rotation"]
        c.target = obj
        c.subtarget = foot_offset_name


def make_arm_ik(obj: bpy.types.Object, suffix: str):
    mode = bpy.context.object.mode
    if mode != "EDIT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="EDIT")

    armature = cast(bpy.types.Armature, obj.data)

    hand_name = f"Hand{suffix}"
    ik_name = f"ArmIK{suffix}"
    lower_name = f"LowerArm{suffix}"
    pole_name = f"ArmPole{suffix}"

    hand = armature.edit_bones[hand_name]
    ik = armature.edit_bones.new(ik_name)
    ik.parent = armature.edit_bones["root"]
    ik.use_connect = False
    ik.head = hand.head
    ik.tail = hand.tail

    pole_head = armature.edit_bones[lower_name].head
    pole = armature.edit_bones.new(pole_name)
    pole.parent = armature.edit_bones["COG"]
    pole.use_connect = False
    pole.head = (pole_head.x, pole_head.y + 0.4, pole_head.z)
    pole.tail = (pole_head.x, pole_head.y + 0.6, pole_head.z)

    lower = armature.edit_bones[lower_name]
    lower.head = (lower.head.x, lower.head.y + 0.01, lower.head.z)

    with enter_pose(obj):
        # IK
        armature.bones.active = armature.bones[lower_name]
        bpy.ops.pose.constraint_add(type="IK")
        c = obj.pose.bones[lower_name].constraints["IK"]
        c.target = obj
        c.subtarget = ik_name
        c.pole_target = obj
        c.pole_subtarget = pole_name
        c.pole_angle = math.pi * (-90) / 180
        c.chain_count = 2
        # HandCopy
        armature.bones.active = armature.bones[hand_name]
        bpy.ops.pose.constraint_add(type="COPY_ROTATION")
        c = obj.pose.bones[hand_name].constraints["Copy Rotation"]
        c.target = obj
        c.subtarget = ik_name


def is_limb(bone: str) -> bool:
    if bone.startswith("LowerArm"):
        return True
    if bone.startswith("LowerLeg"):
        return True
    if "Metacarpal" in bone:
        return True
    if "Proximal" in bone:
        return True
    if "Intermediate" in bone:
        return True
    if "Distal" in bone:
        return True
    return False


def make_finger_bend(obj: bpy.types.Object, finger_name: str, suffix: str):
    mode = bpy.context.object.mode
    if mode != "EDIT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="EDIT")

    armature = cast(bpy.types.Armature, obj.data)

    hand_name = f"Hand{suffix}"
    proximal_name = f"{finger_name}Proximal{suffix}"
    intermediate_name = f"{finger_name}Intermediate{suffix}"
    distal_name = f"{finger_name}Distal{suffix}"
    bend_name = f"Bend{finger_name}{suffix}"

    hand = armature.edit_bones[hand_name]
    proximal = armature.edit_bones[proximal_name]
    distal = armature.edit_bones[distal_name]

    bend = armature.edit_bones.new(bend_name)
    bend.parent = hand
    bend.use_connect = False
    bend.head = proximal.head
    bend.head.z += 0.02
    bend.tail = bend.head
    bend.tail.x = distal.tail.x
    bend.roll = proximal.roll

    def copy_rot(src_name: str, dst_name: str):
        armature.bones.active = armature.bones[dst_name]
        bpy.ops.pose.constraint_add(type="COPY_ROTATION")
        c = obj.pose.bones[dst_name].constraints["Copy Rotation"]
        c.target = obj
        c.subtarget = src_name
        c.target_space = "LOCAL"
        c.owner_space = "LOCAL"

    with enter_pose(obj):
        bend_pose = obj.pose.bones[bend_name]
        bend_pose.rotation_mode = "ZYX"
        bend_pose.lock_rotation[1] = True
        bend_pose.lock_rotation[2] = True
        copy_rot(bend_name, proximal_name)
        copy_rot(bend_name, intermediate_name)
        copy_rot(bend_name, distal_name)


def create(context, rig: bool):
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

    # root
    root = get_or_create_bone(armature, "root")
    root.tail = (0, 1, 0)
    humanoid.create(armature, root)

    # fix roll
    def to_rad(degree: float) -> float:
        return math.pi * degree / 180

    for k, roll in ROLL_MAP.items():
        armature.edit_bones[k].roll = to_rad(roll)

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

    armature.humanoid.left_thumb_metacarpal = "ThumbMetacarpal.L"
    armature.humanoid.left_thumb_proximal = "ThumbProximal.L"
    armature.humanoid.left_thumb_distal = "ThumbDistal.L"
    armature.humanoid.left_index_proximal = "IndexProximal.L"
    armature.humanoid.left_index_intermediate = "IndexIntermediate.L"
    armature.humanoid.left_index_distal = "IndexDistal.L"
    armature.humanoid.left_middle_proximal = "MiddleProximal.L"
    armature.humanoid.left_middle_intermediate = "MiddleIntermediate.L"
    armature.humanoid.left_middle_distal = "MiddleDistal.L"
    armature.humanoid.left_ring_proximal = "RingProximal.L"
    armature.humanoid.left_ring_intermediate = "RingIntermediate.L"
    armature.humanoid.left_ring_distal = "RingDistal.L"
    armature.humanoid.left_little_proximal = "LittleProximal.L"
    armature.humanoid.left_little_intermediate = "LittleIntermediate.L"
    armature.humanoid.left_little_distal = "LittleDistal.L"

    armature.humanoid.right_thumb_metacarpal = "ThumbMetacarpal.R"
    armature.humanoid.right_thumb_proximal = "ThumbProximal.R"
    armature.humanoid.right_thumb_distal = "ThumbDistal.R"
    armature.humanoid.right_index_proximal = "IndexProximal.R"
    armature.humanoid.right_index_intermediate = "IndexIntermediate.R"
    armature.humanoid.right_index_distal = "IndexDistal.R"
    armature.humanoid.right_middle_proximal = "MiddleProximal.R"
    armature.humanoid.right_middle_intermediate = "MiddleIntermediate.R"
    armature.humanoid.right_middle_distal = "MiddleDistal.R"
    armature.humanoid.right_ring_proximal = "RingProximal.R"
    armature.humanoid.right_ring_intermediate = "RingIntermediate.R"
    armature.humanoid.right_ring_distal = "RingDistal.R"
    armature.humanoid.right_little_proximal = "LittleProximal.R"
    armature.humanoid.right_little_intermediate = "LittleIntermediate.R"
    armature.humanoid.right_little_distal = "LittleDistal.R"

    if rig:
        # setup rig
        with enter_pose(obj):
            for b in obj.pose.bones:
                b.rotation_mode = "ZYX"
                if is_limb(b.name):
                    b.lock_rotation[1] = True
                    b.lock_rotation[2] = True

        make_inverted_pelvis(obj)
        make_leg_ik(obj, ".L")
        make_leg_ik(obj, ".R")
        make_arm_ik(obj, ".L")
        make_arm_ik(obj, ".R")
        make_finger_bend(obj, "Index", ".L")
        make_finger_bend(obj, "Middle", ".L")
        make_finger_bend(obj, "Ring", ".L")
        make_finger_bend(obj, "Little", ".L")
        make_finger_bend(obj, "Index", ".R")
        make_finger_bend(obj, "Middle", ".R")
        make_finger_bend(obj, "Ring", ".R")
        make_finger_bend(obj, "Little", ".R")

    # to object mode
    mode = context.object.mode
    if mode != "OBJECT":
        print(f"enter EDIT mode from {mode} mode")
        bpy.ops.object.mode_set(mode="OBJECT")


class CreateHumanoid(bpy.types.Operator):
    """CreateHumanoidArmature"""

    bl_idname = "humanoid.create"
    bl_label = "Create Humanoid"
    bl_options = {"REGISTER", "UNDO"}
    bl_icon = "OUTLINER_OB_ARMATURE"
    bl_menu = "VIEW3D_MT_armature_add"

    rig: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        create(context, self.rig)
        return {"FINISHED"}
