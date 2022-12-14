# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from abc import abstractmethod


# ==================================================================================================
# -- classes ---------------------------------------------------------------------------------------
# ==================================================================================================

class PhysicalLoop:
    """
    This is the abstract template class for Physical-Loop Attack,
    waiting for the derived class to implement the details
    """

    def __init__(self, vehicle, attacker):
        self.vehicle = vehicle
        self.attacker = attacker

    def loop(self, phys_scene, target_output):
        """
        This is the template method describing one loop for Physical Loop Attack
        :param phys_scene: the physical scene such as the whole front view of the vehicle
        :return: the physical scene under adversarial attack
        """

        ## step1: 1st sensor capture (physical scene => digital scene)
        dig_scene = self.sensor_capture(phys_scene)

        ## step2: region extraction (digital scene => digital target)
        target_mask = self.mask_target_generate(dig_scene)
        dig_target = self.region_extract(dig_scene, target_mask)

        ## step3: perturbation generation (digital target => adversarial perturbation)
        adv_mask = self.mask_adv_generate(dig_target)
        adv_perb = self.perb_generate(dig_target, adv_mask)

        ## step4~8: inner loop (optimze adversarial perturbation)
        while not self.inner_loop_failed():  # if inner attack loop failed, loop end
            self._inner_loop(dig_scene, target_mask, target_output,
                             dig_target, adv_mask, adv_perb)
            if self.inner_loop_succeeded():  # if inner attack loop succeeded, early stop
                break
            else:  # else, update something for next inner loop
                self.inner_loop_update()

        ## step9: one last inner loop (get the physical scene under adversarial attack)
        adv_phys_scene = self._inner_loop(dig_scene, target_mask, target_output,
                                          dig_target, adv_mask, adv_perb, required_optimize=False)

        return adv_phys_scene

    def _inner_loop(self, dig_scene, target_mask, target_output,
                    dig_target, adv_mask, adv_perb, required_optimize=True):
        ## step4: perturbation apply (adversarial perturbation => adversarial target)
        adv_target = self.perb_apply(dig_target, adv_mask, adv_perb)
        ## step5: digital replacing (adversarial target => adversarial digital scene)
        adv_dig_scene = self.dig_replace(dig_scene, adv_target, target_mask)
        ## step6: physical replacing (adversarial digital scene => adversarial physical scene)
        adv_phys_scene = self.phys_replace(adv_dig_scene)
        if required_optimize:
            ## step7: 2nd sensor capture (adversarial physical scene => adversarial digital scene)
            adv_dig_scene = self.sensor_capture(adv_phys_scene)
            ## step8: perturbation optimization (dummy perturbation => optimized perturbation)
            done = self.perb_optimize(adv_dig_scene, target_output)
            return done
        else:
            return adv_phys_scene

    @abstractmethod
    def inner_loop_failed(self):
        failed = False

        return failed

    @abstractmethod
    def inner_loop_succeeded(self):
        succeeded = True

        return succeeded

    @abstractmethod
    def inner_loop_update(self):
        pass

    @abstractmethod
    def sensor_capture(self, phys_scene):
        dig_scene = None
        return dig_scene

    @abstractmethod
    def region_extract(self, scene, mask):
        target = None

        return target

    @abstractmethod
    def mask_target_generate(self, scene):
        mask = None

        return mask

    @abstractmethod
    def mask_adv_generate(self, scene):
        mask = None

        return mask

    @abstractmethod
    def dig_replace(self, dig_scene, adv_target, mask):
        adv_dig_scene = None
        return adv_dig_scene

    @abstractmethod
    def phys_replace(self, dig_scene):
        phys_scene = None
        return phys_scene

    @abstractmethod
    def perb_generate(self, target, mask):
        perb = self.attacker.init(target, mask)
        return perb

    @abstractmethod
    def perb_apply(self, target, mask, perb):
        adv_target = None
        return adv_target

    @abstractmethod
    def perb_optimize(self, adv_dig_scene, target_output):
        done = True

        output, loss, done = self.attacker.step(adv_dig_scene, target_output)

        return done


class DefaultPhysicalLoop(PhysicalLoop):
    """
    This the default continuous loop class for Physical-Loop Attack,
    which implements each abstract method in the easiest way, e.g.
    capturing sensor is the front camera, attack target is the billboard in the front
    which can be located by 4 corners' coordinate(box coordinate), perturb region is the whole area
    of the attack target,
    """

    def __init__(self, vehicle, attacker, target_box):
        super().__init__(vehicle, attacker)
        self.target_box = target_box

    def inner_loop_failed(self):
        return self.attacker.attack_failed()

    def inner_loop_succeeded(self):
        return self.attacker.attack_succeeded()

    def inner_loop_update(self):
        return self.attacker.attack_update()

    def sensor_capture(self, phys_scene):
        return self.camera_capture(phys_scene, which="front")

    def camera_capture(self, phys_scene, which="front"):
        return self.vehicle.get_sensor_output(phys_scene, "camera", which)

    def region_extract(self, scene, mask):
        import numpy as np
        target = []
        for m in mask:
            target.append(
                np.multiply(scene, m)
            )
        return target

    def mask_target_generate(self, scene):
        perspective_box = self._get_perspective_target_box()

        import numpy as np
        mask = np.zeros_like(scene, dtype=np.uint8)
        target_mask = self._fill_mask_with_box(mask, perspective_box)
        bgr_mask = self._fill_mask_with_box(mask, perspective_box, reverse=True)
        return target_mask, bgr_mask

    def _get_perspective_target_box(self):
        from adept.transforms import CoordinateTransformer
        transformer = CoordinateTransformer()
        perspective_box = transformer.transform(
            entity=self.target_box,
            fro="world", to="pixel", state=self.vehicle.get_state(),
            image_width=self.vehicle.get_config("front_camera_width"),
            image_height=self.vehicle.get_config("front_camera_height")
        )
        return perspective_box

    def _fill_mask_with_box(self, mask, box, reverse=False):
        import numpy as np
        import cv2
        area = np.array([
            box["top_left"]["c"].tolist(),
            box["top_right"]["c"].tolist(),
            box["bottom_right"]["c"].tolist(),
            box["bottom_left"]["c"].tolist()
        ])
        cv2.fillPoly(mask, area, (1, 1, 1))
        if reverse:
            return np.ones_like(mask, dtype=np.uint8) - mask

    def mask_adv_generate(self, scene):
        import numpy as np
        return np.ones_like(scene, dtype=np.uint8)

    def dig_replace(self, dig_scene, adv_target, mask):
        pass

    def phys_replace(self, dig_scene):
        pass

    def perb_generate(self, target, mask):
        pass

    def perb_apply(self, target, mask, perb):
        pass

    def perb_optimize(self, adv_dig_scene, target_output):
        pass
