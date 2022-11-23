# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from adept.transforms import Coordinate, Pose
from adept.vehicles import Vector
from adept.envs import Env


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Vehicle(ABC):
    """
    This is the abstract template class for (Autonomous) Vehicle, which consists of four modules,
    including sensing module, perception module, planning module, control module,
    waiting for the derived class to implement the details
    """

    def __init__(self, env: Env, model):
        self.env = env
        self.model = model

        self._init_state()
        self._init_config()

    @abstractmethod
    def _init_config(self):
        # TODO: read vehicle's configuration from files and store into self.config_map
        self.config_map = {}

    def get_config(self, attr):
        return self.config_map[attr] if attr in self.config_map else None

    @abstractmethod
    def _init_state(self):
        self.state = None

    def get_state(self):
        return self.state

    @abstractmethod
    def get_sensor_output(self, phys_scene, **kwargs):
        sensor_output = None

        return sensor_output

    @abstractmethod
    def get_perception_input(self):
        pass

    @abstractmethod
    def get_perception_output(self):
        pass

    @abstractmethod
    def get_planning_input(self):
        pass

    @abstractmethod
    def get_planning_output(self):
        pass

    @abstractmethod
    def get_control_input(self):
        control_input = None

        return control_input

    @abstractmethod
    def apply_control(self, control_input):
        pass


class End2EndVehicle(Vehicle):
    """
    This is the basic class for end-to-end autonomous vehicle
    """

    def __init__(self, env, model):
        super().__init__(env, model)

    def _init_config(self):
        self.config_map = {
            "wheel_base": 2.9,

        }

    def _init_state(self):
        pass

    def get_sensor_output(self, phys_scene, **kwargs):
        pass

    def get_perception_input(self):
        pass

    def get_perception_output(self):
        pass

    def get_planning_input(self):
        pass

    def get_planning_output(self):
        pass

    def get_control_input(self):
        pass

    def apply_control(self, control_input):
        pass


class VehicleState(ABC):
    """
    This is the abstract record class for vehicle's state
    note that: the state is represented by a pair/tuple/list/map
    of several elements, and so, it has to be iterative
    """

    def __init__(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass


class BaseVehicleState(VehicleState):
    """
    This is the basic state for vehicle, which only consists of two parts,
    one is position(coordinate), and the other is pose
    """

    def __init__(self, coord: Coordinate, pose: Pose):
        super().__init__()
        self.coord = coord
        self.pose = pose

    def _is_key_for_coord(self, key):
        return key == 0 or key == 'c' or key == 'coord'

    def _is_key_for_pose(self, key):
        return key == 1 or key == 'p' or key == 'pose'

    def __getitem__(self, key):
        if self._is_key_for_coord(key):
            return self.coord
        elif self._is_key_for_pose(key):
            return self.pose
        else:
            raise KeyError("The key " + key + " is unsupported")


class SimpleDynamicsVehicleState(BaseVehicleState):
    """
    This is the class for simple dynamics vehicle state, derived from base vehicle state
    which only appends one dynamics property: velocity
    """

    def __init__(self, coord: Coordinate, pose: Pose, velocity: Vector):
        super().__init__(coord, pose)
        self.velocity = velocity

    def _is_key_for_velocity(self, key):
        return key == 2 or key == 'v' or key == 'velocity'

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            if self._is_key_for_velocity(key):
                return self.velocity
            else:
                raise KeyError("The key " + key + " is unsupported")


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def load_vehicle_model(path, device=None):
    import torch
    model = torch.load(path)

    if device == "gpu":
        model.to(torch.device("cuda") if torch.cuda.is_available() else "cpu")
    elif device == "cpu":
        model.to(torch.device("cpu"))

    return model
