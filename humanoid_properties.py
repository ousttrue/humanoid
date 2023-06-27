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
    "left_thumb_metacarpal",
    "left_thumb_proximal",
    "left_thumb_distal",
    "left_index_proximal",
    "left_index_intermediate",
    "left_index_distal",
    "left_middle_proximal",
    "left_middle_intermediate",
    "left_middle_distal",
    "left_ring_proximal",
    "left_ring_intermediate",
    "left_ring_distal",
    "left_little_proximal",
    "left_little_intermediate",
    "left_little_distal",
    "right_thumb_metacarpal",
    "right_thumb_proximal",
    "right_thumb_distal",
    "right_index_proximal",
    "right_index_intermediate",
    "right_index_distal",
    "right_middle_proximal",
    "right_middle_intermediate",
    "right_middle_distal",
    "right_ring_proximal",
    "right_ring_intermediate",
    "right_ring_distal",
    "right_little_proximal",
    "right_little_intermediate",
    "right_little_distal",
]


class HumanoidProperties(bpy.types.PropertyGroup):
    hips: bpy.props.StringProperty(name="hips")
    spine: bpy.props.StringProperty(name="spine")
    chest: bpy.props.StringProperty(name="chest")
    neck: bpy.props.StringProperty(name="neck")
    head: bpy.props.StringProperty(name="head")
    # arm(8)
    left_shoulder: bpy.props.StringProperty(name="left_shoulder")
    left_upper_arm: bpy.props.StringProperty(name="left_upper_arm")
    left_lower_arm: bpy.props.StringProperty(name="left_lower_arm")
    left_hand: bpy.props.StringProperty(name="left_hand")
    right_shoulder: bpy.props.StringProperty(name="right_shoulder")
    right_upper_arm: bpy.props.StringProperty(name="right_upper_arm")
    right_lower_arm: bpy.props.StringProperty(name="right_lower_arm")
    right_hand: bpy.props.StringProperty(name="right_hand")
    # leg(8)
    left_upper_leg: bpy.props.StringProperty(name="left_upper_leg")
    left_lower_leg: bpy.props.StringProperty(name="left_lower_leg")
    left_foot: bpy.props.StringProperty(name="left_foot")
    left_toes: bpy.props.StringProperty(name="left_toes")
    right_upper_leg: bpy.props.StringProperty(name="right_upper_leg")
    right_lower_leg: bpy.props.StringProperty(name="right_lower_leg")
    right_foot: bpy.props.StringProperty(name="right_foot")
    right_toes: bpy.props.StringProperty(name="right_toes")
    # fingers(30)
    left_thumb_metacarpal: bpy.props.StringProperty(name="left_thumb_metacarpal")
    left_thumb_proximal: bpy.props.StringProperty(name="left_thumb_proximal")
    left_thumb_distal: bpy.props.StringProperty(name="left_thumb_distal")
    left_index_proximal: bpy.props.StringProperty(name="left_index_proximal")
    left_index_intermediate: bpy.props.StringProperty(name="left_index_intermediate")
    left_index_distal: bpy.props.StringProperty(name="left_index_distal")
    left_middle_proximal: bpy.props.StringProperty(name="left_middle_proximal")
    left_middle_intermediate: bpy.props.StringProperty(name="left_middle_intermediate")
    left_middle_distal: bpy.props.StringProperty(name="left_middle_distal")
    left_ring_proximal: bpy.props.StringProperty(name="left_ring_proximal")
    left_ring_intermediate: bpy.props.StringProperty(name="left_ring_intermediate")
    left_ring_distal: bpy.props.StringProperty(name="left_ring_distal")
    left_little_proximal: bpy.props.StringProperty(name="left_little_proximal")
    left_little_intermediate: bpy.props.StringProperty(name="left_little_intermediate")
    left_little_distal: bpy.props.StringProperty(name="left_little_distal")

    right_thumb_metacarpal: bpy.props.StringProperty(name="right_thumb_metacarpal")
    right_thumb_proximal: bpy.props.StringProperty(name="right_thumb_proximal")
    right_thumb_distal: bpy.props.StringProperty(name="right_thumb_distal")
    right_index_proximal: bpy.props.StringProperty(name="right_index_proximal")
    right_index_intermediate: bpy.props.StringProperty(name="right_index_intermediate")
    right_index_distal: bpy.props.StringProperty(name="right_index_distal")
    right_middle_proximal: bpy.props.StringProperty(name="right_middle_proximal")
    right_middle_intermediate: bpy.props.StringProperty(
        name="right_middle_intermediate"
    )
    right_middle_distal: bpy.props.StringProperty(name="right_middle_distal")
    right_ring_proximal: bpy.props.StringProperty(name="right_ring_proximal")
    right_ring_intermediate: bpy.props.StringProperty(name="right_ring_intermediate")
    right_ring_distal: bpy.props.StringProperty(name="right_ring_distal")
    right_little_proximal: bpy.props.StringProperty(name="right_little_proximal")
    right_little_intermediate: bpy.props.StringProperty(
        name="right_little_intermediate"
    )
    right_little_distal: bpy.props.StringProperty(name="right_little_distal")
