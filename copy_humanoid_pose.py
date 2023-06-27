from typing import Optional, Tuple, Iterable, cast
import math
import contextlib
import struct
import bpy
import mathutils  # type: ignore
import json
from . import humanoid_properties

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
}


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
            "extensionsUsed": ["VRMC_vrm_animation"],
            "extensions": {
                "VRMC_vrm_animation": {
                    "humanoid": {
                        "humanBones": {},
                        "frame": {},
                    },
                    "specVersion": "1.0",
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
            self.gltf["extensions"]["VRMC_vrm_animation"]["humanoid"]["humanBones"][
                bone_name
            ] = {"node": index}
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
                        m = (
                            mathutils.Matrix.Rotation(math.radians(180.0), 4, "Z")
                            @ m
                        )
                    t, r, s = m.decompose()

                    frame = self.gltf["extensions"]["VRMC_vrm_animation"]["humanoid"][
                        "frame"
                    ]
                    frame[human_bone] = [r.x, r.y, r.z, r.w]
                    if human_bone == "hips":
                        frame["translation"] = [
                            t.x * self.to_meter,
                            t.z * self.to_meter,
                            t.y * self.to_meter,
                        ]

    def to_json(self) -> str:
        return json.dumps(self.gltf, indent=2)


def glb_bytes(json_chunk: bytes, bin_chunk: bytes) -> Iterable[bytes]:
    def chunk_size(chunk: bytes) -> Tuple[int, int]:
        chunk_size = len(chunk)
        padding = 4 - chunk_size % 4
        return chunk_size, padding

    json_chunk_size, json_chunk_padding = chunk_size(json_chunk)
    bin_chunk_size, bin_chunk_padding = chunk_size(bin_chunk)
    total_size = (
        12
        + (8 + json_chunk_size + json_chunk_padding)
        + (8 + bin_chunk_size + bin_chunk_padding)
    )

    yield struct.pack("III", 0x46546C67, 2, total_size)
    yield struct.pack("II", json_chunk_size + json_chunk_padding, 0x4E4F534A)
    yield json_chunk
    yield b" " * json_chunk_padding
    yield struct.pack("II", bin_chunk_size + bin_chunk_padding, 0x004E4942)
    yield bin_chunk
    yield b"\0" * bin_chunk_padding


# def main():
#     ret = bpy.ops.import_anim.bvh(  # type: ignore
#         filepath=sys.argv[1],
#         use_fps_scale=True,
#         update_scene_duration=True,
#     )
#     if ret != FINISHED:
#         raise Exception()

#     bpy.context.scene.frame_current = 450

#     builder = Builder()
#     o = bpy.context.active_object  # type: ignore

#     builder.get_tpose(o)
#     builder.get_current_pose(o)

#     # to clip board
#     text = builder.to_json()
#     print(text)
#     pyperclip.copy(text)

#     # to vrm
#     if len(sys.argv) > 2:
#         dst = pathlib.Path(sys.argv[2])
#         with dst.open("wb") as w:
#             for b in glb_bytes(json.dumps(builder.gltf).encode("utf-8"), b""):
#                 w.write(b)


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
