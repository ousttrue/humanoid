from typing import Optional, BinaryIO, Tuple, Iterable, cast
import math
import contextlib
import struct
import pathlib
import bpy
import mathutils  # type: ignore
import json
import sys
import io


FINISHED = {"FINISHED"}

HUMANOID_MAP = {
    "Hips": "hips",
    "Spine": "spine",
    "Spine1": "chest",
    "Neck": "neck",
    "Head": "head",
    "LeftShoulder": "leftShoulder",
    "LeftArm": "leftUpperArm",
    "LeftForeArm": "leftLowerArm",
    "LeftHand": "leftHand",
    "RightShoulder": "rightShoulder",
    "RightArm": "rightUpperArm",
    "RightForeArm": "rightLowerArm",
    "RightHand": "rightHand",
    "LeftUpLeg": "leftUpperLeg",
    "LeftLeg": "leftLowerLeg",
    "LeftFoot": "leftFoot",
    "LeftToeBase": "leftToes",
    "RightUpLeg": "rightUpperLeg",
    "RightLeg": "rightLowerLeg",
    "RightFoot": "rightFoot",
    "RightToeBase": "rightToes",
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
    def __init__(self) -> None:
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
            "extensionsUsed": ["VRMC_vrm"],
            "extensions": {
                "VRMC_vrm": {
                    "humanoid": {"humanBones": {}},
                    "meta": {
                        "allowAntisocialOrHateUsage": True,
                        "allowExcessivelySexualUsage": True,
                        "allowExcessivelyViolentUsage": True,
                        "allowPoliticalOrReligiousUsage": True,
                        "allowRedistribution": True,
                        "authors": ["python bvh pose"],
                        "avatarPermission": "everyone",
                        "commercialUsage": "corporation",
                        "copyrightInformation": "python bvh pose",
                        "creditNotation": "required",
                        "licenseUrl": "",
                        "modification": "allowModificationRedistribution",
                        "name": "pose",
                        "version": "1",
                    },
                    "specVersion": "1.0",
                },
                "VRMC_vrm_pose": {},
            },
        }

    def get_root(self) -> dict:
        return self.gltf["nodes"][0]

    def add_child(self, parent: Optional[dict], node: dict) -> int:
        index = len(self.gltf["nodes"])
        if not parent:
            parent = self.get_root()
        if "children" not in parent:
            parent["children"] = []
        parent["children"].append(index)
        self.gltf["nodes"].append(node)
        return index

    def traverse(self, b, parent, *, indent: str):
        m = b.matrix_local
        if b.parent:
            m = b.parent.matrix_local.inverted() @ m
        t, r, s = m.decompose()
        # print(f'{indent}{b}: {t} {r}')
        node = {
            "name": b.name,
            "translation": [t.x, t.y, t.z],
            "rotation": [r.x, r.y, r.z, r.w],
        }
        index = self.add_child(parent, node)
        bone_name = HUMANOID_MAP.get(b.name)
        if bone_name:
            self.gltf["extensions"]["VRMC_vrm"]["humanoid"]["humanBones"][bone_name] = {
                "node": index
            }
        else:
            print(f"{b.name} not found")

        for child in b.children:
            self.traverse(child, node, indent=indent + "  ")

        return node

    def get_tpose(self, o: bpy.types.Object):
        def get_roots(a: bpy.types.Armature):
            for bone in a.bones:
                if not bone.parent:
                    yield bone

        for root in get_roots(o.data):
            root_node = self.traverse(root, None, indent="")

    def get_current_pose(self, o: bpy.types.Object):
        pose = cast(bpy.types.Pose, o.pose)  # type: ignore
        with enter_pose(o):
            for b in pose.bones:
                human_bone = HUMANOID_MAP.get(b.name)
                if human_bone:
                    init = b.bone.matrix
                    m = b.matrix
                    if b.parent:
                        m = b.parent.matrix.inverted() @ m
                    else:
                        m = mathutils.Matrix.Rotation(math.radians(-90.0), 4, "X") @ m
                    t, r, s = m.decompose()
                    bone_pose = {
                        "rotation": [r.x, r.y, r.z, r.w],
                    }
                    if not b.parent:
                        bone_pose["translation"] = [t.x, t.y, t.z]
                    self.gltf["extensions"]["VRMC_vrm_pose"][human_bone] = bone_pose

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


def main():
    ret = bpy.ops.import_anim.bvh(  # type: ignore
        filepath=sys.argv[1],
        use_fps_scale=True,
        update_scene_duration=True,
    )
    if ret != FINISHED:
        raise Exception()

    bpy.context.scene.frame_current = 450

    builder = Builder()
    o = bpy.context.active_object  # type: ignore

    builder.get_tpose(o)
    builder.get_current_pose(o)

    # to clip board
    text = builder.to_json()
    print(text)
    pyperclip.copy(text)

    # to vrm
    if len(sys.argv) > 2:
        dst = pathlib.Path(sys.argv[2])
        with dst.open("wb") as w:
            for b in glb_bytes(json.dumps(builder.gltf).encode("utf-8"), b""):
                w.write(b)


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
        self.report({"INFO"}, f"{type(context.active_object.data)}")
        context.window_manager.clipboard = "copy pose"
        return {"FINISHED"}
