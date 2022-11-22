"""
the attacks package contains all functions for ADS adversarial attack
which basically includes two closed-loops:
=======================
one is physical loop
=> attack autonomous vehicles in a physical world (simulation world if in the simulation environment)
=> so we have to deal with physical-world-and-digital-world gaps
=> as for images, there contains two types of transforms between two worlds:
=>  1. physical-to-digital: camera capture(which is affected by vehicle pose, noise, weather, etc)
=>  2. digital-to-physical: print(which is affected by printability of the printer)
=> and the whole attack process for one image frame contains three transforms above: [1,2,1] in order
=> so when attacking image-fed model, the adversarial image should go through all of them to guarantee attack effects
=======================
the other is continuous loop
=> attack autonomous vehicles in a continuous process, considering vehicle's control feedback in each attack step
=> even if we successfully attacked the model's output, the final output of vehicle's control is not exactly the same
=> so we have to update the target in each attack step with respect to vehicle's state(including pose and dynamics)
=> because the state will decide the vehicle's final control output
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from ._physical_loop import PhysicalLoop, DefaultPhysicalLoop
from ._continous_loop import ContinuousLoop, DefaultContinuousLoop
from ._attack import Attacker, FGSMAttacker, PGDAttacker


# ==================================================================================================
# -- all -------------------------------------------------------------------------------------------
# ==================================================================================================

__all__ = [  # user interface and other dependent packages
    "PhysicalLoop", "DefaultPhysicalLoop",
    "ContinuousLoop", "DefaultContinuousLoop",
    "Attacker", "FGSMAttacker", "PGDAttacker",
]