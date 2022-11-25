# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from adept.transforms import Point, Box2D


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Coordinate(ABC):
    """
    This is the abstract class for Coordination,
    which consists of a pair/tuple/list/map of base elements to locate an entity,
    and so, it has to be iterative
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def tolist(self):
        pass


class Coordinate2D(Coordinate):
    """
    This is the base class for 2-dim(x,y) Coordination
    """

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def _is_key_for_x(self, key):
        return key == 0 or key == 'x' or key == 'X'

    def _is_key_for_y(self, key):
        return key == 1 or key == 'y' or key == 'Y'

    def __getitem__(self, key):
        if self._is_key_for_x(key):
            return self.x
        elif self._is_key_for_y(key):
            return self.y
        else:
            raise KeyError("The key " + key + " is unsupported")

    def tolist(self):
        return [self.x, self.y]


class Coordinate3D(Coordinate2D):
    """
    This is the base class for 3-dim(x,y,z) Coordination
    """

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y)
        self.z = z

    def _is_key_for_z(self, key):
        return key == 2 or key == 'z' or key == 'Z'

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            if self._is_key_for_z(key):
                return self.z
            else:
                raise KeyError("The key " + key + " is unsupported")

    def tolist(self):
        return super().tolist().append(self.z)


class WorldCoordinate(Coordinate3D):
    """
    This is the class for World Coordination,
    which consists of three dimensions: x,y,z and locates the entity in the world
    note that:
        1. the original point is not that important as for world coordination, which may be the center of earth,
        depending on the environment
        2. if the world coordination belongs to Cartesian Coordinates, then its direction is often right-handed
    """

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)


class VehicleCoordinate(Coordinate3D):
    """
    This is the class for Vehicle Coordination,
    which consists of three dimensions: x,y,z and locates the entity in the vehicle's view
    note that:
        1. the original point is at the vehicle's mass center(often the center of the back axle)
        2. the x-axis points to right, the y-axis points to front, and the z-axis points to top (right-handed)
        3. the vehicle coordinate can be transformed from world coordination
        through rotation matrix R and translation vector T, and vise versa
    """
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)

    def trans_from(self, wc: WorldCoordinate, R, T):
        pass

    def trans_to(self, R, T) -> WorldCoordinate:
        pass


class CameraCoordinate(Coordinate3D):
    """
    This is the class for Camera Coordination,
    which consists of three dimensions: x,y,z and locates the entity in the camera
    note that:
        1. the original point is at the camera's optical center
        2. the x-axis points to right, the y-axis points to top, and the z-axis points to front (left-handed)
        3. the camera coordinate can be transformed from world coordination
        through rotation matrix R, translation vector T, and z-dim reverse, and vise versa
    """

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)

    def trans_from(self, wc: WorldCoordinate, R, T):
        pass

    def trans_to(self, R, T) -> WorldCoordinate:
        pass


class ImagePlaneCoordinate(Coordinate2D):
    """
    This is the class for Image Plane Coordination,
    which consists of two dimensions: x,y and locates the entity in the image plane
    note that:
        1. the original point is at the plane's geometry center
        2. the x-axis points to right and the y-axis points to top
        3. the image plane coordinate can be transformed from camera coordination
        through focal scaling F and z-dim normalization,  and vice versa
    """

    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def trans_from(self, cc: CameraCoordinate, F):
        pass

    def trans_to(self, F, z) -> CameraCoordinate:
        pass


class ImagePixelCoordinate(Coordinate2D):
    """
    This is the class for Image Pixel Coordination,
    which consists of two dimensions: x,y and locates the entity in the digital image pixel matrix
    note that:
        1. the original point is at the image's top-left corner
        2. the x-ais points to right, and the y-axis points to bottom
        3. the image pixel plane coordinate can be transformed from image plane coordination
        through translation vector T, scaling factor S and y-dim reverse
    """

    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def trans_from(self, ipc: ImagePlaneCoordinate, T, S):
        pass

    def trans_to(self, T, S) -> ImagePlaneCoordinate:
        pass


class CoordinateTransformer:
    """
    This is the functional class, defining a useful function: transform(fro, to)
    in which it will transform any coordinate 'fro' to any coordinate 'to'
    """

    def __init__(self):
        pass

    def transform(self, entity, fro, to, **kwargs):
        if fro == "world" and to == "pixel":
            return self._transform_world2pixel(
                entity=entity,
                x=kwargs["state"]["c"]["x"], y=kwargs["state"]["c"]["y"], z=kwargs["state"]["c"]["z"],
                pitch=kwargs["state"]["p"]["p"], yaw=kwargs["state"]["p"]["y"], roll=kwargs["state"]["p"]["r"],
                h=kwargs["image_height"], w=kwargs["image_width"]
            )

    def translate(self, entity, dx=0, dy=0):
        pass

    def _transform_world2pixel(self, entity, x, y, z, pitch, yaw, roll, h, w):
        import math
        import numpy as np
        front_vec, left_vec, up_vec = [1, 0, 0], [0, 1, 0], [0, 0, 1]

        def trans_vector(vector, pitch, yaw, roll):
            def trans_pitch(x, y, z, pitch):
                newx = x * math.cos(pitch) - z * math.sin(pitch)
                newy = y
                newz = x * math.sin(pitch) + z * math.cos(pitch)
                return newx, newy, newz

            def trans_yaw(x, y, z, yaw):
                newx = x * math.cos(yaw) - y * math.sin(yaw)
                newy = x * math.sin(yaw) + y * math.cos(yaw)
                newz = z
                return newx, newy, newz

            def trans_roll(x, y, z, roll):
                newx = x
                newy = z * math.sin(roll) + y * math.cos(roll)
                newz = z * math.cos(roll) - y * math.sin(roll)
                return newx, newy, newz

            x, y, z = vector[0], vector[1], vector[2]
            x, y, z = trans_pitch(x, y, z, pitch)
            x, y, z = trans_yaw(x, y, z, yaw)
            x, y, z = trans_roll(x, y, z, roll)
            return [x, y, z]

        pitch, yaw, roll = pitch / 180 * math.pi, yaw / 180 * math.pi, roll / 180 * math.pi
        front_vec = trans_vector(front_vec, pitch, yaw, roll)
        left_vec = trans_vector(left_vec, pitch, yaw, roll)
        up_vec = trans_vector(up_vec, pitch, yaw, roll)

        points = []
        for point in entity:
            coord = point["c"]
            point_vec = [coord["x"]-x, coord["y"]-y, coord["z"]-z]

            tmp_f, tmp_x, tmp_y = np.dot(point_vec, front_vec), \
                      np.dot(point_vec, left_vec), np.dot(point_vec, up_vec)
            if tmp_f < 0:
                return None

            tan_x = tmp_x / tmp_f
            tan_y = tmp_y / tmp_f

            px = (tan_x * 0.5 * w) + w / 2
            py = -(tan_y * 0.5 * h) + h / 2

            points.append(Point(Coordinate2D(x=px, y=py)))

        if len(points) == 4:  # box
            return Box2D(*points)
