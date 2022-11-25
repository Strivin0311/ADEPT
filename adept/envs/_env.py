# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod
from adept.envs.carla import load_carla, load_client, load_world


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Env(ABC):
    """
    This is the abstract template class for (Simulation) Environment,
    waiting for the derived class to implement the details
    """

    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def tick(self, times=1):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def scene_retrieve(self):
        scene = None

        return scene


class BaseCarlaEnv(Env, ABC):
    """
    This is the basic class for environment in carla
    which implements the necessary initial work to do
    """

    def __init__(self, root, world_name, version=None,
                 ip='localhost', port=2000, timeout=10,
                 sync=True, delta=0.0, print_path=False):
        super().__init__()
        self.carla_root = root
        self.world_name = world_name
        self.carla_version = version

        ## step0: load carla, client, world and something else before initializing actors
        load_carla(root=self.carla_root, version=self.carla_version, print_path=print_path)
        self.client = load_client(ip=ip, port=port, timeout=timeout)
        self.world = load_world(self.client, world_name=self.world_name, sync=sync, delta=delta)

        ## step1: init others after actors, like some configurations
        self._init_before_actors()
        ## step2: init actors
        self.actor_map = {}
        self._init_actors()
        ## step3: init others after actors, such as weather
        self._init_after_actors()

    @abstractmethod
    def _init_actors(self):
        pass

    def _init_before_actors(self):
        pass

    def _init_after_actors(self):
        pass

    def _close_actors(self):
        for actor in self.actor_map:
            self.actor_map[actor].destroy()

    def _close_others(self):
        pass

    def scene_retrieve(self):
        pass

    def get_world(self):
        return self.world

    def get_actor(self, key):
        if key in self.actor_map:
            return self.actor_map[key]

    @abstractmethod
    def get_ego_actor(self):
        pass

    @ abstractmethod
    def run(self):
        pass

    def tick(self, times=1, sleep=0.0):
        for _ in range(times):
            self.world.tick()
            if sleep > 0.0:
                import time
                time.sleep(sleep)

    def close(self):
        self._close_actors()
        self._close_others()
