# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import ABC, abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class Attacker(ABC):
    """
    This is the abstract template class for Adversarial Attack,
    waiting for the derived class to implement the details
    """

    def __init__(self, target_model):
        self.target_model = target_model

        self.perb = None

    def _attack(self, target_input, target_output):
        """
        This is the template method describing the whole attack process
        :return: done: True if attack succeeded, otherwise False |
                 perturbation: the optimized perturbation adding to target_input to attack
                 the target_model to output the target_output
        """
        done = False
        self.attack_init()  # initialize the perturbation before optimizing

        while not self.attack_failed():  # if attack failed, end optimizing and return False
            self.attack_optimizer()  # optimize the perturbation using certain algorithm

            if self.attack_succeeded():  # if attack succeeded, end optimizing and return True
                done = True
                break
            else:  # else, update something for next optimization
                self.attack_update()

        return done, self.attack_retrieve()

    @abstractmethod
    def attack_failed(self):
        failed = False

        return failed

    @abstractmethod
    def attack_succeeded(self):
        succeeded = True

        return succeeded

    @abstractmethod
    def attack_retrieve(self):
        return self.perb

    @abstractmethod
    def attack_init(self):
        self.perb = None

    @abstractmethod
    def attack_update(self):
        pass

    @abstractmethod
    def attack_optimizer(self):
        self.perb = None


class FGSMAttacker(Attacker):
    def __init__(self, target_model):
        super().__init__(target_model)

    def attack_failed(self):
        pass

    def attack_succeeded(self):
        pass

    def attack_retrieve(self):
        pass

    def attack_init(self):
        pass

    def attack_update(self):
        pass

    def attack_optimizer(self):
        pass


class PGDAttacker(Attacker):
    def __init__(self, target_model):
        super().__init__(target_model)

    def attack_failed(self):
        pass

    def attack_succeeded(self):
        pass

    def attack_retrieve(self):
        pass

    def attack_init(self):
        pass

    def attack_update(self):
        pass

    def attack_optimizer(self):
        pass