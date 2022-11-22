"""
the carla package contains all functions corresponding to carla (current version is 0.9.13)
such as loading world, spawning actors, changing weather, etc
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from ._load import load_carla, load_client, load_world
from ._setter import set_weather, set_spectator, add_actor
from ._getter import get_blueprint, get_color, get_transform, \
    get_location_relative_to, get_rotation_relative_to, get_raw_image
from ._enum import CarlaVersion, WorldName, ActorAttr, CameraAttr, VehicleType, SensorType, WeatherType, \
    ActorAddMode, TransformAddMode


# ==================================================================================================
# -- all -------------------------------------------------------------------------------------------
# ==================================================================================================

__all__ = [  # user interface and other dependent packages
    "load_carla", "load_client", "load_world",
    "set_weather", "set_spectator", "add_actor",
    "get_blueprint", "get_color", "get_transform",
    "get_location_relative_to", "get_rotation_relative_to", "get_raw_image",
    "CarlaVersion", "WorldName", "ActorAttr", "CameraAttr",
    "VehicleType", "SensorType", "WeatherType",
    "ActorAddMode", "TransformAddMode",
]