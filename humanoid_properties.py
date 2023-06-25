import bpy

PROP_NAMES = [
    "hips",
    "spine",
    "chest",
    "neck",
    "head",
    "left_shoulder",
    "left_upper_arm",
    "left_lower_arm",
    "left_hand",
    "right_shoulder",
    "right_upper_arm",
    "right_lower_arm",
    "right_hand",
    "left_upper_leg",
    "left_lower_leg",
    "left_foot",
    "left_toes",
    "right_upper_leg",
    "right_lower_leg",
    "right_foot",
    "right_toes",
]


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
