# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Pose(ABC):
    """
    This is the abstract class for Pose,
    which consists of a pair/tuple/list/map of base elements to
    describe an entity(rigid body)'s pose(i.e. the rotation with reference to the standard direction)
    and so, it has to be iterative
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass


class EulerAngle(Pose):
    """
    This the class for Euler Angle
    which consists of three dimensions: pitch, roll, yaw and describes an entity(rigid body)'s pose by three rotates
    note that:
        1. the pitch is to describe the rotation on the x-axis
        2. the roll is to describe the rotation on the y-axis
        3. the yaw is to describe the rotation on the z-axis
    """

    def __init__(self, pitch=0.0, roll=0.0, yaw=0.0):
        super().__init__()
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw

    def _is_key_for_pitch(self, key):
        return key == 0 or key == 'pitch' or key == 'p' or key == 'P'

    def _is_key_for_roll(self, key):
        return key == 1 or key == 'roll' or key == 'r' or key == 'R'

    def _is_key_for_yaw(self, key):
        return key == 2 or key == 'yaw' or key == 'y' or key == 'Y'

    def __getitem__(self, key):
        if self._is_key_for_pitch(key):
            return self.pitch
        elif self._is_key_for_roll(key):
            return self.roll
        elif self._is_key_for_yaw(key):
            return self.yaw
        else:
            raise KeyError("The key " + key + " is unsupported")


class Quaternion(Pose):
    """
    This is the class for Quaternion q
    which consists of two parts: 1-dimension real part w, 3-dimension imaginary part v=[x,y,z]
    and describes an entity(rigid body)'s pose by one rotate
    note that:
        1. a 3-dim vector P can be represented as a quaternion which has zero real part, i.e. w = 0
        2. qPq^-1 represents rotating P around unit vector A by angle θ, where q = w + v = cos(θ/2) + A * sin(θ/2)
        3. q1q2 = (w1w2 - v1v2) + w1v2 + w2v1 + v1xv2, which represents rotate by q2 and then by q1
    """

    def __init__(self, w=0.0, x=0.0, y=0.0, z=0.0):
        super().__init__()
        self.w = w  # real part
        self.v = [x, y, z]  # virtual part

    def _is_key_for_real(self, key):
        return key == 0 or key == 'w' or key == 's' or key == 'r' or key == 'real'

    def _is_key_for_img(self, key):
        return key == 'i' or key == 'v' or key == 'img' or key == 'imaginary'

    def _is_key_for_x(self, key):
        return key == 1 or key == 'x'

    def _is_key_for_y(self, key):
        return key == 2 or key == 'y'

    def _is_key_for_z(self, key):
        return key == 3 or key == 'z'

    def __getitem__(self, key):
        if self._is_key_for_real(key):
            return self.w
        elif self._is_key_for_img(key):
            return self.v
        elif self._is_key_for_x(key):
            return self.v[0]
        elif self._is_key_for_y(key):
            return self.v[1]
        elif self._is_key_for_z(key):
            return self.v[2]
        else:
            raise KeyError("The key " + key + " is unsupported")

    def __mul__(self, other):
        import numpy as np

        if isinstance(other, (int, float)):
            return Quaternion(other*self.w, *((other*np.array(self.v)).tolist()))
        elif isinstance(other, Quaternion):
            w1, v1 = self.w, np.array(self.v)
            w2, v2 = other.w, np.array(self.v)

            w = w1*w2 - v1.dot(v2)
            v = (w1*v2 + w2*v1 + np.cross(v1,v2)).tolist()
            return Quaternion(w, *v)
        else:
            raise TypeError("The type " + type(other) + " is unsupported")


class PoseTransformer:
    """
    This is the functional class, defining a useful function: transform(fro, to)
    in which it will transform any pose 'fro' to any pose 'to'
    """

    def __init__(self):
        pass

    def transform(self, fro, to, **kwargs):
        pass