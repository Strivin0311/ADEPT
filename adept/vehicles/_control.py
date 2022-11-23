# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Controller(ABC):
    """
    This is the abstract template class for Vehicle Control Module,
    waiting for the derived class to implement the details
    """

    def __init__(self):
        pass

    @abstractmethod
    def path_following(self):
        pass

    @abstractmethod
    def trajectory_following(self):
        pass


class PurePursuitController(Controller):
    """
    This is the class for geometry-based model-free(kinematic-model) controller
    which uses pure pursuit algorithm as the control strategy for path following only

    note that: pure pursuit is one of the geometry-based control strategies of path following
    for the kinematic model, proved to be an indispensable tool for vehicle control owing to
    its simple implementation and satisfactory performance, assuming that the path has no curvature
    and the vehicle speed is constant(potentially negative)

    paper cite: Coulter, R. Craig. Implementation of the pure pursuit path tracking algorithm.
    Carnegie-Mellon UNIV Pittsburgh PA Robotics INST, 1992.

    paper link: https://apps.dtic.mil/sti/pdfs/ADA255524.pdf
    """

    def __init__(self, vehicle, planner, ld=2.6, lf_gain=0.0,):
        super().__init__()

        ## hold the vehicle and the planner
        self.vehicle = vehicle
        self.planner = planner

        ## init some control hyper-parameters
        self.ld = ld  # lookahead distance
        self.lf_gain = lf_gain  # look forward gain

        ## the start idx of the key point in the reference path
        self.start = 0

    def get_current_key_point(self):
        return self.planner.get_target_path()[self.start]

    def path_following(self):
        ## step0: get the necessary state(x,y,yaw,v) components of the vehicle
        state = self.vehicle.get_state()
        x, y, yaw, v = state['coord']['x'], state['coord']['y'], state['pose']['yaw'], state['v']
        ## step1: calculate the look-forward distance
        ## considering lookahead distance and velocity
        lf = self.lf_gain * v + self.ld
        ## step2: find the target key point(x_ref, y_ref) in the reference path
        if self.start == 0:  # init start point
            ref_path = self.planner.get_target_path_from(self.start)
            p, self.start = ref_path.get_nearest_point(x, y)
        ref_path = self.planner.get_target_path_from(self.start)
        p, self.start = ref_path.get_nearest_point(x, y, away_from=lf)
        xr, yr = p["c"]["x"], p["c"]["y"]
        ## step3: calculate the look-forward angle alpha
        from math import atan2, sin
        alpha = atan2(yr-y, xr-x) - yaw
        ## step4: calculate the target steering angle theta
        wheel_base = self.vehicle.get_config("wheel_base")
        theta = atan2(2 * wheel_base * sin(alpha), lf)

        return theta

    def trajectory_following(self):
        pass


class ControlInput:
    """
    This is the record class to describe the control input
    """

    def __init__(self):
        pass