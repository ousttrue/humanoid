from typing import Tuple, List, Any, Callable, Sequence
import bpy
import datetime

class Color:
    r: float
    g: float
    b: float
    h: float
    s: float
    v: float
    hsv: 'float triplet'
    is_wrapped: bool
    is_frozen: bool
    is_valid: bool
    def __init__(self, rgb: '3d vector') -> None: ... # noqa
    def copy(self) -> Color: ... # noqa
    def freeze(self) -> None: ... # noqa
    def from_scene_linear_to_srgb(self) -> Color: ... # noqa
    def from_srgb_to_scene_linear(self) -> Color: ... # noqa
    def from_scene_linear_to_xyz_d65(self) -> Color: ... # noqa
    def from_xyz_d65_to_scene_linear(self) -> Color: ... # noqa
    def from_scene_linear_to_aces(self) -> Color: ... # noqa
    def from_aces_to_scene_linear(self) -> Color: ... # noqa
    def from_scene_linear_to_rec709_linear(self) -> Color: ... # noqa
    def from_rec709_linear_to_scene_linear(self) -> Color: ... # noqa


class Euler:
    x: float
    y: float
    z: float
    order: str
    is_wrapped: bool
    is_frozen: bool
    is_valid: bool
    def __init__(self, angles: '3d vector', order: str) -> None: ... # noqa
    def zero(self) -> None: ... # noqa
    def to_matrix(self) -> Matrix: ... # noqa
    def to_quaternion(self) -> Quaternion: ... # noqa
    def rotate_axis(self, axis: str, angle: float) -> None: ... # noqa
    def rotate(self, other: 'Any') -> None: ... # noqa
    def make_compatible(self) -> None: ... # noqa
    def copy(self) -> Euler: ... # noqa
    def freeze(self) -> None: ... # noqa


class Matrix:
    median_scale: float
    translation: 'Vector'
    row: 'Matrix Access'
    col: 'Matrix Access'
    is_identity: bool
    is_negative: bool
    is_orthogonal: bool
    is_orthogonal_axis_vectors: bool
    is_wrapped: bool
    is_frozen: bool
    is_valid: bool
    def __init__(self, rows: '2d number sequence') -> None: ... # noqa
    def determinant(self) -> 'Any': ... # noqa
    def decompose(self) -> 'class': ... # noqa
    def zero(self) -> Matrix: ... # noqa
    def identity(self) -> None: ... # noqa
    def transpose(self) -> None: ... # noqa
    def transposed(self) -> Matrix: ... # noqa
    def normalize(self) -> None: ... # noqa
    def normalized(self) -> Matrix: ... # noqa
    def invert(self, fallback: 'Any') -> None: ... # noqa
    def inverted(self, fallback: 'Any') -> Matrix: ... # noqa
    def invert_safe(self) -> None: ... # noqa
    def inverted_safe(self) -> Matrix: ... # noqa
    def adjugate(self) -> None: ... # noqa
    def adjugated(self) -> Matrix: ... # noqa
    def to_2x2(self) -> Matrix: ... # noqa
    def to_3x3(self) -> Matrix: ... # noqa
    def to_4x4(self) -> Matrix: ... # noqa
    def resize_4x4(self) -> None: ... # noqa
    def rotate(self, other: 'Any') -> None: ... # noqa
    def to_euler(self, order: str, euler_compat: 'Any') -> Euler: ... # noqa
    def to_quaternion(self) -> Quaternion: ... # noqa
    def to_scale(self) -> Vector: ... # noqa
    def to_translation(self) -> Vector: ... # noqa
    def lerp(self, other: 'Any', factor: float) -> Matrix: ... # noqa
    def copy(self) -> Matrix: ... # noqa
    def freeze(self) -> None: ... # noqa


class Quaternion:
    w: float
    x: float
    y: float
    z: float
    magnitude: float
    angle: float
    axis: ':class:`Vector`'
    is_wrapped: bool
    is_frozen: bool
    is_valid: bool
    def __init__(self, *args) -> None: ... # noqa
    def identity(self) -> Quaternion: ... # noqa
    def negate(self) -> Quaternion: ... # noqa
    def conjugate(self) -> None: ... # noqa
    def conjugated(self) -> Quaternion: ... # noqa
    def invert(self) -> None: ... # noqa
    def inverted(self) -> Quaternion: ... # noqa
    def normalize(self) -> None: ... # noqa
    def normalized(self) -> Quaternion: ... # noqa
    def to_euler(self, order: str, euler_compat: 'Any') -> Euler: ... # noqa
    def to_matrix(self) -> Matrix: ... # noqa
    def to_axis_angle(self) -> 'class': ... # noqa
    def to_swing_twist(self) -> 'class': ... # noqa
    def to_exponential_map(self) -> Vector: ... # noqa
    def cross(self, other: 'Any') -> Quaternion: ... # noqa
    def dot(self, other: 'Any') ->  float: ... # noqa
    def rotation_difference(self, other: 'Any') -> Quaternion: ... # noqa
    def slerp(self, other: 'Any', factor: float) -> Quaternion: ... # noqa
    def rotate(self, other: 'Any') -> None: ... # noqa
    def make_compatible(self) -> None: ... # noqa
    def freeze(self) -> None: ... # noqa
    def copy(self) -> Quaternion: ... # noqa


class Vector:
    x: float
    y: float
    z: float
    w: float
    length: float
    length_squared: float
    magnitude: float
    is_wrapped: bool
    is_frozen: bool
    is_valid: bool
    def __init__(self, seq: 'sequence of numbers') -> None: ... # noqa
    def zero(self) -> None: ... # noqa
    def negate(self) -> None: ... # noqa
    def normalize(self) -> None: ... # noqa
    def normalized(self) -> Vector: ... # noqa
    def resize(self) -> None: ... # noqa
    def resized(self) -> Vector: ... # noqa
    def to_2d(self) -> Vector: ... # noqa
    def resize_2d(self) -> None: ... # noqa
    def to_3d(self) -> Vector: ... # noqa
    def resize_3d(self) -> None: ... # noqa
    def to_4d(self) -> Vector: ... # noqa
    def resize_4d(self) -> None: ... # noqa
    def to_tuple(self, precision: int) ->  tuple: ... # noqa
    def to_track_quat(self, track: str, up: str) -> Quaternion: ... # noqa
    def orthogonal(self) -> Vector: ... # noqa
    def reflect(self, mirror: 'Any') -> Vector: ... # noqa
    def cross(self, other: 'Any') -> Vector: ... # noqa
    def dot(self, other: 'Any') ->  float: ... # noqa
    def angle(self, other: 'Any', fallback: 'Any') ->  float: ... # noqa
    def angle_signed(self, other: 'Any', fallback: 'Any') ->  float: ... # noqa
    def rotation_difference(self, other: 'Any') -> Quaternion: ... # noqa
    def project(self, other: 'Any') -> Vector: ... # noqa
    def lerp(self, other: 'Any', factor: float) -> Vector: ... # noqa
    def slerp(self, other: 'Any', factor: float, fallback: 'Any') -> Vector: ... # noqa
    def rotate(self, other: 'Any') -> None: ... # noqa
    def freeze(self) -> None: ... # noqa
    def copy(self) -> Vector: ... # noqa


