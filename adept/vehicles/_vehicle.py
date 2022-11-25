# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from adept.envs.carla import retrieve_from, apply_control
from adept.transforms import Coordinate, Pose, WorldCoordinate, EulerAngle
from adept.vehicles import Vector, Vector3D


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Vehicle(ABC):
    """
    This is the abstract template class for (Autonomous) Vehicle, which consists of four modules,
    including sensing module, perception module, planning module, control module,
    waiting for the derived class to implement the details
    """

    def __init__(self, env, model):
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
    def get_sensor_output(self, phys_scene, sensor, **kwargs):
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

    def __init__(self, env, model, device="gpu"):
        super().__init__(env, model)
        import torch
        self.device = torch.device("cuda") \
            if torch.cuda.is_available() and device == "gpu" else torch.device("cpu")

    def _init_config(self):
        pass

    def _init_state(self):
        x, y, z, p, y, r, vx, vy, vz = self._get_ego_vehicle_state()
        self.state = SimpleDynamicsVehicleState(
            coord=WorldCoordinate(x=x, y=y, z=z),
            pose=EulerAngle(pitch=p, yaw=y, roll=r),
            velocity=Vector3D(vx, vy, vz)
        )

    def get_state(self):
        x, y, z, p, y, r, vx, vy, vz = self._get_ego_vehicle_state()
        self.state["c"]["x"], self.state["c"]["y"], self.state["c"]["z"] = x, y, z
        self.state["p"]["p"], self.state["p"]["y"], self.state["p"]["r"] = p, y, r
        self.state["v"]["x"], self.state["v"]["y"], self.state["v"]["z"] = vx, vy, vz
        return self.state

    def _get_ego_vehicle_state(self):
        ego_vehicle = self.env.get_ego_actor()
        location = retrieve_from(actor=ego_vehicle, about="location")
        rotation = retrieve_from(actor=ego_vehicle, about="rotation")
        velocity = retrieve_from(actor=ego_vehicle, about="velocity")
        return location.x, location.y, location.z, \
               rotation.pitch, rotation.yaw, rotation.roll, \
               velocity.x, velocity.y, velocity.z

    def get_sensor_output(self, phys_scene, sensor="camera", **kwargs):
        import numpy as np
        import torch
        self.phys_scene = torch.from_numpy(np.array(phys_scene)).float().div_(255).to(self.device)

    def get_control_input(self):
        import torch

        ## step1: get steering model's control output
        ## based on phys_scene from sensor output
        with torch.no_grad():
            predict_steer = float(self.model(self.phys_scene))

        ## step2: get whole control input
        ## from the predicted steer and current velocity
        ego_vehicle = self.env.get_ego_actor()
        velocity = retrieve_from(actor=ego_vehicle, about="velocity")
        return self.env.controller.get_control_from(
            steer=predict_steer, velocity=velocity)

    def apply_control(self, control_input):
        apply_control(self.env.get_ego_actor(),
                      control_input)

    def get_perception_input(self):
        pass

    def get_perception_output(self):
        pass

    def get_planning_input(self):
        pass

    def get_planning_output(self):
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
