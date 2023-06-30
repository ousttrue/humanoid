from typing import Optional, Tuple, Iterable, cast
import math
import bpy
import mathutils  # type: ignore
import json
from . import humanoid_properties
from .enter_pose_mode import enter_pose

VRM_ANIMATION = "VRMC_vrm_animation"
VRM_POSE = "VRMC_vrm_pose"


class Builder:
    def __init__(self, armature: bpy.types.Armature, to_meter: float) -> None:
        self.tree = humanoid_properties.HumanTree(armature)
        self.to_meter = to_meter
        assert isinstance(armature, bpy.types.Armature)

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

    def add_gltf_node(self, gltf_parent: Optional[dict], gltf_node: dict) -> int:
        index = len(self.gltf["nodes"])
        if not gltf_parent:
            # root
            gltf_parent = self.gltf["nodes"][0]
        if "children" not in gltf_parent:
            gltf_parent["children"] = []
        gltf_parent["children"].append(index)
        self.gltf["nodes"].append(gltf_node)
        return index

    def _traverse_tpose(self, b, gltf_parent, *, indent: str):
        m = b.matrix_local
        parent = self.tree.get_parent(b)
        if parent:
            m = parent.matrix_local.inverted() @ m
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
        index = self.add_gltf_node(gltf_parent, gltf_node)
        vrm_bone = self.tree.vrm_from_name(b.name)
        if vrm_bone:
            # bone node mapping
            self.gltf["extensions"][VRM_ANIMATION]["humanoid"]["humanBones"][
                vrm_bone
            ] = {"node": index}
            # print(f"{b.name}: {bone_prop}")
        else:
            print(f"{b.name} not found")

        for child in self.tree.get_children(b):
            self._traverse_tpose(child, gltf_node, indent=indent + "  ")

        return gltf_node

    def get_tpose(self, o: bpy.types.Object):
        hips = self.tree.bone_from_prop("hips")
        self._traverse_tpose(hips, None, indent="")

    def get_current_pose(self, o: bpy.types.Object):
        pose = cast(bpy.types.Pose, o.pose)  # type: ignore
        with enter_pose(o):
            for b in pose.bones:
                vrm_bone = self.tree.vrm_from_name(b.name)
                if vrm_bone:
                    init = b.bone.matrix
                    m = b.matrix
                    parent = self.tree.get_parent(b)
                    print(b, parent)
                    if parent:
                        m = parent.matrix.to_4x4().inverted() @ m
                    else:
                        # pass
                        m = mathutils.Matrix.Rotation(math.radians(180.0), 4, "Z") @ m
                    t, r, s = m.decompose()

                    vrm_pose = self.gltf["extensions"][VRM_ANIMATION]["extensions"][
                        VRM_POSE
                    ]["humanoid"]
                    vrm_pose["rotations"][vrm_bone] = [r.x, r.y, r.z, r.w]
                    if vrm_bone == "hips":
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
