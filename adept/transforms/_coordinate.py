# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


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

    def transform(self, fro, to, **kwargs):
        pass
