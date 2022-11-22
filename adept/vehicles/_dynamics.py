# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Vector(ABC):
    """
    This is the abstract class for any vector in Vehicle Dynamics,
    which consists of a pair/tuple/list/map of scalar components,
    and so, it is iterative
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass


class Vector2D(Vector):
    """
    This is the base class for 2-dim(x,y) Vector
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


class Vector3D(Vector2D):
    """
    This is the base class for 3-dim(x,y,z) Vector
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
