# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class ContinuousLoop(ABC):
    """
    This is the abstract template class for Continuous-Loop Attack,
    waiting for the derived class to implement the details
    """

    def __init__(self, phys_loop, env, vehicle, planner, controller):
        self.phys_loop = phys_loop
        self.env = env
        self.vehicle = vehicle
        self.planner = planner
        self.controller = controller

    def loop(self):
        """
        This is the template method describing the whole loop for Continuous Loop Attack
        :return: True if task succeeded, otherwise False, and maybe something else
        """

        self.loop_init()  # some initial work before loop

        while not self.task_failed():  # if task failed, then loop end
            ## step1: let environment retrieve physcial scene
            ## based on current state of the vehicle
            phys_scene = self.scene_phys_retrieve()
            ## step2: let controller compute the target control input
            ## based on current state of the vehicle and the target path of the planner
            target_input = self.input_controller_compute()
            ## step3: let physical loop generate the adversarial physcial scene
            ## based on original physical scene and target control input
            adv_phys_scene = self.scene_adv_generate(phys_scene, target_input)
            ## step4: let vehicle compute the adversarial control input
            ## based on generated adversarial physical scene
            adv_input = self.input_vehicle_compute(adv_phys_scene)
            ## step5: let vehicle update its state
            ## based on the current state and input
            self.state_vehicle_update(adv_input)

            if self.task_succeeded():  # if task succeeded, then early stop
                break
            else:  # else, do some update work before next loop
                self.loop_update()

        return self.loop_end()  # some final work before return

    def scene_adv_generate(self, phys_scene, target_input):
        adv_phys_scene = self.phys_loop.loop(phys_scene, target_input)

        return adv_phys_scene

    @abstractmethod
    def loop_init(self):
        self.done = False
        self.state = self.state_vehicle_retrieve()  # initial state of the vehicle
        self.epoch = 0

    @abstractmethod
    def loop_update(self):
        self.state = self.state_vehicle_retrieve()  # current state of the vehicle
        self.epoch += 1

    @abstractmethod
    def loop_end(self):
        return self.done

    @abstractmethod
    def task_failed(self):
        failed = False

        return failed

    @abstractmethod
    def task_succeeded(self):
        succeeded = True

        self.done = True

        return succeeded

    @abstractmethod
    def scene_phys_retrieve(self):
        phys_scene = None

        return phys_scene

    @abstractmethod
    def input_controller_compute(self):
        input = None

        return input

    @abstractmethod
    def input_vehicle_compute(self, phys_scene):
        input = None

        return input

    @abstractmethod
    def state_vehicle_retrieve(self):
        state = None

        return state

    @abstractmethod
    def state_vehicle_update(self, input):
        pass


class DefaultContinuousLoop(ContinuousLoop):
    """
    This the default continuous loop class for Continuous-Loop Attack,
    which implements each abstract method in the easiest way, e.g.
    the task being failed or succeeded only depends on the final_time and final_state
    """

    def __init__(self, phys_loop, env, vehicle, planner, controller,
                 max_time=3600):
        super().__init__(phys_loop, env, vehicle, planner, controller)

        self.max_time = max_time  # the lifetime of one ContiLoop object, default 3600(1 hour)

        self.time = None
        self.final_time = None
        self.done = None
        self.state = None

    def loop_init(self):
        self.time = 0  # initial timestamp
        self.final_time = self.max_time  # at most the whole lifetime
        self.done = False  # if attack succeeded
        self.state = self.state_vehicle_retrieve()  # initial state of the vehicle

    def loop_update(self):
        self.time += 1
        self.state = self.state_vehicle_retrieve()

    def loop_end(self):
        return self.done

    def task_failed(self):
        return self.time > self.final_time

    def task_succeeded(self):
        ## step1: get the current state of the vehicle
        state = self.state_vehicle_retrieve()
        ## step2: let planner tell if the current state is reached the {final_state}
        self.done = self.planner.in_final_states(state)

        return self.done

    def scene_phys_retrieve(self):
        return self.env.scene_retrieve()

    def input_controller_compute(self):
        ## step1: get the current state of the vehicle
        state = self.state_vehicle_retrieve()
        ## step2: get the target path from the planner
        target_path = self.planner.get_target_path()
        ## step3: get the target control input from the controller
        ## using some kind of path following algorithm
        target_control_input = self.controller.path_following(state, target_path)

        return target_control_input

    def input_vehicle_compute(self, phys_scene):
        return self.vehicle.get_control_input(phys_scene)

    def state_vehicle_retrieve(self):
        return self.vehicle.get_state()

    def state_vehicle_update(self, input):
        self.vehicle.apply_control(input)
