# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def get_blueprint(world, key, mode="filter", choose="random", **kwargs):
    blueprint_library = world.get_blueprint_library()
    if mode == "find":
        return blueprint_library.find(key)
    elif mode == "filter":
        bps = blueprint_library.filter(key)
        if len(bps) is not 0:
            if choose == "random":
                import random
                return random.choice(bps)
            elif isinstance(choose, int) and choose < len(bps):
                return bps[0]
        return None
    return None


def get_transform(world, mode, **kwargs):
    if mode == "random":  # random transform from available spawn points in the map
        import random
        return random.choice(world.get_map().get_spawn_points())
    elif isinstance(mode, int):  # ith transform from available spawn points in the map
        spawn_points = world.get_map().get_spawn_points()
        if mode < len(spawn_points):
            return spawn_points[mode]
        return None

    ## get the specific transform depending on the location and/or rotation
    transform, location, rotation = None, None, None
    import carla
    if "location" in mode:
        location = carla.Location(
            x=kwargs["x"] if "x" in kwargs else 0.0,
            y=kwargs["y"] if "y" in kwargs else 0.0,
            z=kwargs["z"] if "z" in kwargs else 0.0
        )
    if "rotation" in mode:
        rotation = carla.Rotation(
            pitch=kwargs["pitch"] if "pitch" in kwargs else 0.0,
            yaw=kwargs["yaw"] if "yaw" in kwargs else 0.0,
            roll=kwargs["roll"] if "roll" in kwargs else 0.0
        )

    if location is not None and rotation is not None:
        transform = carla.Transform(location=location, rotation=rotation)
    elif location is not None:
        transform = carla.Transform(location=location)
    elif rotation is not None:
        transform = carla.Transform(rotation=rotation)

    return transform


def get_color(blueprint, mode="random", **kwargs):
    if not blueprint.has_attribute('color') or \
            not blueprint.get_attribute('color').is_modifiable:  # color can't be set
        return None
    if mode == "random":  # get random color from blueprint's recommended values
        import random
        return random.choice(blueprint.get_attribute('color').recommended_values)
    elif mode in ("rgb", "RGB", "rgba", "RGBA"):
        import carla
        return carla.Color(
            r=kwargs["r"] if "r" in kwargs else 0,
            g=kwargs["g"] if "g" in kwargs else 0,
            b=kwargs["b"] if "b" in kwargs else 0,
            a=kwargs["a"] if "a" in kwargs else 255
        )
    return None


def get_location_relative_to(ref_actor=None, dx=0.0, dy=0.0, dz=0.0):
    if ref_actor is not None:
        location = ref_actor.get_location()
        x = location.x + dx
        y = location.y + dy
        z = location.z + dz
        return x, y, z
    else:
        return dx, dy, dz


def get_rotation_relative_to(ref_actor=None, dpitch=0.0, dyaw=0.0, droll=0.0):
    if ref_actor is not None:
        rotation = ref_actor.get_rotation
        pitch = rotation.pitch + dpitch
        yaw = rotation.yaw + dyaw
        roll = rotation.roll + droll
        return pitch, yaw, roll
    else:
        return dpitch, dyaw, droll


def get_raw_image(carla_image, format="bgr"):
    import numpy as np
    import cv2

    raw_img = np.array(carla_image.raw_data)  # take raw data from carla image
    raw_img = np.reshape(raw_img, newshape=(carla_image.height, carla_image.width, 4))  # 4 channels: BGRA
    if format == "bgr":
        return cv2.cvtColor(raw_img, cv2.BGRA2BGR) # BGRA => RGB
    elif format == "rgb":
        return cv2.cvtColor(raw_img, cv2.BGRA2RGB)  # BGRA => BGR
    elif format == "gray":
        return cv2.cvtColor(raw_img, cv2.BGRA2GRAY) # BGRA => GRAY
    elif format == "hsv":
        return cv2.cvtColor(raw_img, cv2.BGRA2HSV) # BGRA => HSV
    elif format == "yuv":
        return cv2.cvtColor(raw_img, cv2.BGRA2YUV)  # BGRA => YUV

    return raw_img  # BGRA
