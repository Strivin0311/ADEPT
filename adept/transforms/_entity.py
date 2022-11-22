# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from ._coordinate import Coordinate, Coordinate2D, Coordinate3D
from typing import List, Union


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class CoordinateEntity(ABC):
    """
    This is the abstract class for entity which can be described only by its components' coordinate
    and so, it is iterative to get each component
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass


class Point(CoordinateEntity):
    """
    This is the class for point, which is the simplest entity with only one coordinate to describe
    """

    def __init__(self, coord: Coordinate):
        super().__init__()
        self.coord = coord

    def __getitem__(self, key):
        if key == 0 or key == 'c' or key == 'coord':
            return self.coord
        else:
            raise KeyError("The key " + key + " is unsupported")

    def distance_from(self, x, y, ord='fro'):
        import numpy as np
        return np.linalg.norm(np.array([
            x - self.coord["x"], y - self.coord["y"]
        ]), ord=ord)


class Line(CoordinateEntity):
    """
    This is the class for a straight line, which needs two points to describe
    one is the start point p0, the other is the end point p1 (po -> p1)
    """

    def __init__(self, p0: Point, p1: Point):
        super().__init__()
        self.p0 = p0
        self.p1 = p1

    def _is_key_for_p0(self, key):
        return key == 0 or key == 'p0'

    def _is_key_for_p1(self, key):
        return key == 1 or key == 'p1'

    def __getitem__(self, key):
        if self._is_key_for_p0(key):
            return self.p0
        elif self._is_key_for_p1(key):
            return self.p1
        else:
            raise KeyError("The key " + key + " is unsupported")


class Box2D(CoordinateEntity):
    """
    This is the class for 2-dim box, which needs four corner points to describe
    note that: the order is started at top-left corner and moved in counter-clockwise direction
    """

    def __init__(self, top_left: Point, top_right: Point,
                 bottom_right: Point, bottom_left: Point):
        super().__init__()
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    def _is_key_for_top_left(self, key):
        return key == 0 or key == 'tl' or key == 'top_left' or key == 'top left'

    def _is_key_for_top_right(self, key):
        return key == 1 or key == 'tr' or key == 'top_right' or key == 'top right'

    def _is_key_for_bottom_right(self, key):
        return key == 2 or key == 'br' or key == 'bottom_right' or key == 'bottom right'

    def _is_key_for_bottom_left(self, key):
        return key == 3 or key == 'bl' or key == 'bottom_left' or key == 'bottom left'

    def __getitem__(self, key):
        if self._is_key_for_top_left(key):
            return self.top_left
        elif self._is_key_for_top_right(key):
            return self.top_right
        elif self._is_key_for_bottom_right(key):
            return self.bottom_right
        elif self._is_key_for_bottom_left(key):
            return self.bottom_left
        else:
            raise KeyError("The key " + key + " is unsupported")


class Box3D(CoordinateEntity):
    """
    This is the class for 3-dim box, which consists of two 2-dim box,
    one is the front box, the other is the back box, and together they represent 8 corner points
    """

    def __init__(self, front_box, back_box):
        super().__init__()
        self.front_box = front_box
        self.back_box = back_box

    def _is_key_for_front(self, key):
        return key == 0 or key == 'f' or key == 'front'

    def _is_key_fro_back(self, key):
        return key == 1 or key == 'b' or key == 'back'

    def __getitem__(self, key):
        if self._is_key_for_front(key):
            return self.front_box
        elif self._is_key_fro_back(key):
            return self.back_box
        else:
            raise KeyError("The key " + key + " is unsupported")


class SamplePath2D(CoordinateEntity):
    """
    This is the class for a sampled path, which needs a list of points in order to describe
    """

    def __init__(self, plist: List[Point]):
        super().__init__()
        self.plist = plist

    def append(self, p: Union[Point, list, tuple]):
        if isinstance(p, Point):
            self.plist.append(p)
        else:
            self.plist.append(Point(Coordinate2D(*p)))

    def get_nearest_point(self, x, y, away_from=0):
        nd, npx, npy, idx = float('inf'), 0, 0, -1
        for i, p in enumerate(self.plist):
            d = p.distance_from(x, y)
            if away_from <= d < nd:
                nd, npx, npy, idx = d, p["c"]["x"], p["c"]["y"], i

        return Point(Coordinate2D(npx, npy)), idx

    def _is_key_for_start(self, key):
        return key == 0 or key == 'begin' or key == 'start'

    def _is_key_for_end(self, key):
        return key == len(self.plist) - 1 or key == -1 or key == 'end' or key == 'last'

    def __getitem__(self, key):
        if self._is_key_for_start(key):
            return self.plist[0]
        elif self._is_key_for_end(key):
            return self.plist[-1]
        elif 1 <= key < len(self.plist):
            return self.plist[key]
        else:
            raise KeyError("The key " + key + " is unsupported")

    def __len__(self):
        return len(self.plist)
