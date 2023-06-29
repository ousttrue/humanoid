from typing import Optional, Tuple, Iterable, cast
import math
import bpy
import mathutils  # type: ignore
import json
from . import humanoid_properties
from .enter_pose_mode import enter_pose

VRM_ANIMATION = "VRMC_vrm_animation"
VRM_POSE = "VRMC_vrm_pose"

PROP_TO_HUMANBONE = {
    "left_shoulder": "leftShoulder",
    "left_upper_arm": "leftUpperArm",
    "left_lower_arm": "leftLowerArm",
    "left_hand": "leftHand",
    "right_shoulder": "rightShoulder",
    "right_upper_arm": "rightUpperArm",
    "right_lower_arm": "rightLowerArm",
    "right_hand": "rightHand",
    "left_upper_leg": "leftUpperLeg",
    "left_lower_leg": "leftLowerLeg",
    "left_foot": "leftFoot",
    "left_toes": "leftToes",
    "right_upper_leg": "rightUpperLeg",
    "right_lower_leg": "rightLowerLeg",
    "right_foot": "rightFoot",
    "right_toes": "rightToes",
    "left_thumb_metacarpal": "leftThumbMetacarpal",
    "left_thumb_proximal": "leftThumbProximal",
    "left_thumb_distal": "leftThumbDistal",
    "left_index_proximal": "leftIndexProximal",
    "left_index_intermediate": "leftIndexIntermediate",
    "left_index_distal": "leftIndexDistal",
    "left_middle_proximal": "leftMiddleProximal",
    "left_middle_intermediate": "leftMiddleIntermediate",
    "left_middle_distal": "leftMiddleDistal",
    "left_ring_proximal": "leftRingProximal",
    "left_ring_intermediate": "leftRingIntermediate",
    "left_ring_distal": "leftRingDistal",
    "left_little_proximal": "leftLittleProximal",
    "left_little_intermediate": "leftLittleIntermediate",
    "left_little_distal": "leftLittleDistal",
    "right_thumb_metacarpal": "rightThumbMetacarpal",
    "right_thumb_proximal": "rightThumbProximal",
    "right_thumb_distal": "rightThumbDistal",
    "right_index_proximal": "rightIndexProximal",
    "right_index_intermediate": "rightIndexIntermediate",
    "right_index_distal": "rightIndexDistal",
    "right_middle_proximal": "rightMiddleProximal",
    "right_middle_intermediate": "rightMiddleIntermediate",
    "right_middle_distal": "rightMiddleDistal",
    "right_ring_proximal": "rightRingProximal",
    "right_ring_intermediate": "rightRingIntermediate",
    "right_ring_distal": "rightRingDistal",
    "right_little_proximal": "rightLittleProximal",
    "right_little_intermediate": "rightLittleIntermediate",
    "right_little_distal": "rightLittleDistal",
}


class Builder:
    def __init__(self, armature: bpy.types.Armature, to_meter: float) -> None:
        self.to_meter = to_meter
        assert isinstance(armature, bpy.types.Armature)
        # custom property
        self.humanoid_map = armature.humanoid
        assert self.humanoid_map

        self.gltf = {
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [
                {
                    "name": "__zup__",
                    "rotation": [-0.7071, 0, 0, 0.7071],
                }
            ],
            "asset": {"version": "2.0"},
            "extensionsUsed": [VRM_ANIMATION, VRM_POSE],
            "extensions": {
                VRM_ANIMATION: {
                    "humanoid": {
                        "humanBones": {},
                    },
                    "specVersion": "1.0",
                    "extensions": {
                        VRM_POSE: {
                            "humanoid": {
                                "translation": [0, 0, 0],
                                "rotations": {},
                            },
                            "expressions": {
                                "preset": {
                                    "happy": 1,
                                    "Aa": 1,
                                }
                            },
                            "lookAt": {
                                "position": [4, 5, 6],
                            },
                        },
                    },
                },
            },
        }

    def get_human_bone(self, bone_name: str) -> Optional[str]:
        for prop in humanoid_properties.PROP_NAMES:
            if getattr(self.humanoid_map, prop) == bone_name:
                human_bone = PROP_TO_HUMANBONE.get(prop)
                if human_bone:
                    return human_bone
                else:
                    return prop

    def add_child(self, gltf_parent: Optional[dict], gltf_node: dict) -> int:
        index = len(self.gltf["nodes"])
        if not gltf_parent:
            # root
            gltf_parent = self.gltf["nodes"][0]
        if "children" not in gltf_parent:
            gltf_parent["children"] = []
        gltf_parent["children"].append(index)
        self.gltf["nodes"].append(gltf_node)
        return index

    def traverse(self, b, gltf_parent, *, indent: str):
        m = b.matrix_local
        if b.parent:
            m = b.parent.matrix_local.inverted() @ m
        t, r, s = m.decompose()
        print(f"{indent}{b}: {t} {r}")
        gltf_node = {
            "name": b.name,
            "translation": [
                t.x * self.to_meter,
                t.y * self.to_meter,
                t.z * self.to_meter,
            ],
            "rotation": [r.x, r.y, r.z, r.w],
        }
        index = self.add_child(gltf_parent, gltf_node)
        bone_name = self.get_human_bone(b.name)
        if bone_name:
            # bone node mapping
            self.gltf["extensions"][VRM_ANIMATION]["humanoid"]["humanBones"][
                bone_name
            ] = {"node": index}
            print(f"{b.name}: {bone_name}")
        else:
            print(f"{b.name} not found")

        for child in b.children:
            self.traverse(child, gltf_node, indent=indent + "  ")

        return gltf_node

    def get_tpose(self, o: bpy.types.Object):
        for bone in o.data.bones:
            if not bone.parent:
                self.traverse(bone, None, indent="")

    def get_current_pose(self, o: bpy.types.Object):
        pose = cast(bpy.types.Pose, o.pose)  # type: ignore
        with enter_pose(o):
            for b in pose.bones:
                human_bone = self.get_human_bone(b.name)
                if human_bone:
                    init = b.bone.matrix
                    m = b.matrix
                    if b.parent:
                        m = b.parent.matrix.inverted() @ m
                    else:
                        m = mathutils.Matrix.Rotation(math.radians(180.0), 4, "Z") @ m
                    t, r, s = m.decompose()

                    vrm_pose = self.gltf["extensions"][VRM_ANIMATION]["extensions"][
                        VRM_POSE
                    ]["humanoid"]
                    vrm_pose["rotations"][human_bone] = [r.x, r.y, r.z, r.w]
                    if human_bone == "hips":
                        vrm_pose["translation"] = [
                            t.x * self.to_meter,
                            t.z * self.to_meter,
                            t.y * self.to_meter,
                        ]

    def to_json(self) -> str:
        return json.dumps(self.gltf, indent=2)


class CopyHumanoidPose(bpy.types.Operator):
    bl_idname = "humanoid.copy_pose"
    bl_label = "Copy Humanoid Pose"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if context.active_object:
            return isinstance(context.active_object.data, bpy.types.Armature)
        return False

    def execute(self, context: bpy.types.Context):
        o = bpy.context.active_object  # type: ignore
        builder = Builder(o.data, 1)

        builder.get_tpose(o)
        builder.get_current_pose(o)

        # to clip board
        text = builder.to_json()
        # print(text)
        self.report({"INFO"}, "copy pose to clipboard")
        context.window_manager.clipboard = text
        return {"FINISHED"}
