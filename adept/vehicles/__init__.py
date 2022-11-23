"""
the vehicles package contains all functions about vehicle itself
such as geometry, architecture, kinematics, dynamics, control, etc
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from ._vehicle import Vehicle, VehicleState, BaseVehicleState, SimpleDynamicsVehicleState, \
    load_vehicle_model, End2EndVehicle
from ._plan import Planner, ReferencePlanner
from ._control import Controller, ControlInput, PurePursuitController
from ._dynamics import Vector, Vector2D, Vector3D


# ==================================================================================================
# -- all -------------------------------------------------------------------------------------------
# ==================================================================================================

__all__ = [  # user interface and other dependent packages
    "Vehicle", "VehicleState", "SimpleDynamicsVehicleState",
    "load_vehicle_model", "End2EndVehicle",
    "Planner", "ReferencePlanner",
    "Controller", "ControlInput", "PurePursuitController",
    "Vector", "Vector2D", "Vector3D"
]