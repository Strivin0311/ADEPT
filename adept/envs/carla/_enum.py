# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================


from enum import Enum, unique


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================


class CarlaVersion(Enum):
    """
    This is the enum class for carla version, whose latest one is 0.9.13
    """

    v_latest = "0.9.13"
    v_0_9_6 = "0.9.6"
    v_0_9_13 = "0.9.13"


@unique
class WorldName(Enum):
    """
    This is the enum class for world(town) name in carla
    """

    town_01 = "Town01"
    town_02 = "Town02"
    town_03 = "Town03"
    town_04 = "Town04"


@unique
class ActorAttr(Enum):
    """
    This is the enum class for actor's attribute in carla
    """

    location = "location"


@unique
class CameraAttr(Enum):
    width = "image_size_x"
    height = "image_size_y"
    horizontal_field = "fov"


@unique
class VehicleType(Enum):
    """
    This is the enum class for vehicle type in carla
    """

    model3 = "model3"


@unique
class SensorType(Enum):
    """
    This is the enum class for RGB camera sensor in carla
    """

    rgb_camera = "sensor.camera.rgb"


@unique
class WeatherType(Enum):
    """
    This is the enum class for weather type in carla
    """

    clear_noon = "ClearNoon"


@unique
class ActorAddMode(Enum):
    """
    This is the enum class of adding types for actors in carla
    """

    random = "random"
    filter = "filter"


@unique
class TransformAddMode(Enum):
    """
    This is the enum class of adding types for transforms in carla
    """

    random = "random"
    location_only = "location"
    rotation_only = "rotation"
    location_and_rotation = "location, rotation"


