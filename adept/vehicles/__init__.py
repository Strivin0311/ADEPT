"""
the vehicles package contains all functions about vehicle itself
such as geometry, architecture, kinematics, dynamics, control, etc
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from ._vehicle import Vehicle, VehicleState, BaseVehicleState, SimpleDynamicsVehicleState
from ._plan import Planner, ReferencePlanner
from ._control import Controller, ControlInput, PurePursuitController
from ._dynamics import Vector, Vector2D, Vector3D


# ==================================================================================================
# -- all -------------------------------------------------------------------------------------------
# ==================================================================================================

__all__ = [  # user interface and other dependent packages
    "Vehicle", "VehicleState", "SimpleDynamicsVehicleState",
    "Planner", "ReferencePlanner",
    "Controller", "ControlInput", "PurePursuitController",
    "Vector", "Vector2D", "Vector3D"
]