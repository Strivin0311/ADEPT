# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from adept.transforms import Coordinate2D, Coordinate3D, Point, SamplePath2D


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Planner(ABC):
    """
    This is the abstract template class for Vehicle Planning Module,
    waiting for the derived class to implement the details
    """

    def __init__(self):
        pass

    @abstractmethod
    def in_final_states(self, state):
        yes = False

        return yes

    @abstractmethod
    def get_target_path(self):
        target_path = []

        return target_path


class ReferencePlanner(Planner):
    """
    This the class for planner which only contains a reference path(read from files)
    and no computation or algorithm
    """

    def __init__(self, ref_path_file, dim=2, split=' ', sample_rate=1):
        super().__init__()

        self.ref_path_file = ref_path_file
        self.dim = dim

        self._read_ref_path(split, sample_rate)

    def _read_ref_path(self, split, sample_rate):
        if self.dim == 2:
            self.path = SamplePath2D([])
        elif self.dim == 3:  # TODO: SamplePath3D
            pass

        cnt = 0
        with open(self.ref_path_file, 'r') as f:
            for line in f:
                if cnt % sample_rate == 0:
                    items = [float(i) for i in line.split(split)[:self.dim]]
                    self.path.append(items)
                cnt += 1

    def in_final_states(self, idx):
        return idx >= len(self.path)

    def get_target_path(self):
        return self.path

    def get_target_path_from(self, start):
        if start >= len(self.path):
            return
        return self.path[start:]

    def dim(self):
        return self.dim
