"""
This script is to let vehicle run by itself without hijack
as a controlled experiment
"""

# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

from adept.envs import BaseCarlaEnv
from adept.envs.carla import add_actor, set_weather, set_spectator, \
    get_location_relative_to, get_rotation_relative_to, get_raw_image, \
    CarlaVersion, WorldName, CameraAttr, SensorType, VehicleType, WeatherType, \
    ActorAddMode, TransformAddMode
from adept.attacks import DefaultContinuousLoop, DefaultPhysicalLoop, PGDAttacker
from adept.vehicles import ReferencePlanner, PurePursuitController, End2EndVehicle, \
    load_vehicle_model
from adept.transforms import Point, Box2D, WorldCoordinate, img_transfer
from adept.view import add_video_writer, save_video_frame, \
    show_image, add_image_queue, get_image_from_queue, put_image_to_queue


# ==================================================================================================
# -- scripts ---------------------------------------------------------------------------------------
# ==================================================================================================

class HijackVehicle(End2EndVehicle):
    def __init__(self, env, model):
        super().__init__(env, model)

    def _init_config(self):
        self.config_map = {
            "wheel_base": 2.9,
            "front_camera_height": self.env.camera_info["front_camera"]["height"],
            "front_camera_width": self.env.camera_info["front_camera"]["width"]
        }


class HijackPhysLoop(DefaultPhysicalLoop):

    def __init__(self, vehicle, attacker, target_box):
        super().__init__(vehicle, attacker, target_box)

    def _get_perspective_target_box(self):
        from adept.transforms import CoordinateTransformer
        transformer = CoordinateTransformer()
        perspective_box = super()._get_perspective_target_box()
        perspective_box = transformer.translate(  # for model's input
            entity=perspective_box, dx=0, dy=-75
        )
        return perspective_box


class HijackContiLoop(DefaultContinuousLoop):

    def __init__(self, phys_loop, env, vehicle, planner, controller):
        super().__init__(phys_loop, env, vehicle, planner, controller)


class HijackCarlaEnv(BaseCarlaEnv):

    def __init__(self, root, world_name, version, ref_path_file):
        super().__init__(root, world_name, version)

    def _init_actors(self):
        ## step1: init ego vehicle
        self.actor_map["ego"] = add_actor(
            world=self.world, key=VehicleType.model3.value,
            mode=ActorAddMode.filter.value, choose=0,
            transform=0,
        )
        ## step2: init cameras
        for camera in self.camera_info:
            info = self.camera_info[camera]
            self.actor_map[camera] = add_actor(
                world=self.world, key=SensorType.rgb_camera.value,
                mode=ActorAddMode.filter.value, choose=0,
                transform=TransformAddMode.location_and_rotation,
                x=info["x"], y=info["y"], z=info["z"],
                pitch=info["pitch"], yaw=info["yaw"], roll=info["roll"],
                specific_attrs={
                    CameraAttr.width.value: info["width"],
                    CameraAttr.height.value: info["height"],
                    CameraAttr.horizontal_field.value: info["fov"]
                }, attach_to=self.actor_map["ego"], listen=info["listen"]
            )

    def _init_before_actors(self):
        self.ref_path_file = ref_path_file
        self._load_camera_info()
        self._load_billboard_info()

    def _init_after_actors(self):
        ## step1: init weather
        set_weather(self.world, WeatherType.clear_noon.value)
        ## step2: init spectator's location and rotation, relative to the ego vehicle's
        x, y, z = get_location_relative_to(ref_actor=self.actor_map["ego"],
                                           dx=0, dy=-6.4, dz=2.0)
        pitch, yaw, roll = get_rotation_relative_to(dpitch=-15.0, dyaw=90.0, droll=0.0)
        set_spectator(self.world, transform=TransformAddMode.location_and_rotation,
                      x=x, y=y, z=z, pitch=pitch, yaw=yaw, roll=roll)

        ## step3: load steering model and init vehicle
        self.model_path = "../../resources/models/NVIDIA model.pkl"
        self.steering_model = load_vehicle_model(self.model_path, device="gpu")
        self.vehicle = HijackVehicle(env=self, model=self.steering_model)
        ## step4: init reference planner
        self.planner = ReferencePlanner(self.ref_path_file, sample_rate=10)  # sample every 10 points
        ## step5: init pure pursuit controller
        self.controller = PurePursuitController(vehicle=self.vehicle, planner=self.planner, lf_gain=0.1)

        ## step6: init attacker
        self.attacker = PGDAttacker(target_model=self.steering_model)
        ## step7: init physical loop and continuous loop
        self.phys_loop = HijackPhysLoop(vehicle=self.vehicle, attacker=self.attacker,
                                           target_box=self.billboard_box)
        self.conti_loop = HijackContiLoop(phys_loop=self.phys_loop, env=self, vehicle=self.vehicle,
                                             planner=self.planner, controller=self.controller)

    def _load_camera_info(self):
        # TODO: use configuration file to read/write in the future

        ## step1: add video writer
        front_writer, front_save_path = add_video_writer(
            width=200, height=200, fps=10, save_path='../../outputs/videos/front'
        )
        back_writer, back_save_path = add_video_writer(
            width=1920, height=1080, fps=10, save_path='../../outputs/videos/back'
        )
        top_writer, top_save_path = add_video_writer(
            width=1920, height=1080, fps=10, save_path='../../outputs/videos/top'
        )
        ## step2: define basic camera information
        self.camera_info = {
            "front_camera": {
                "width": 200, "height": 200, "fov": 90,
                "x": 1.5, "y": 0.0, "z": 2.4,
                "pitch": 0.0, "yaw": 0.0, "roll": 0.0,
                "video_writer": front_writer, "video_save_path": front_save_path,
                "queue": add_image_queue()
            },
            "back_camera": {
                "width": 1920, "height": 1080, "fov": 110,
                "x": -5.0, "y": 0.0, "z": 3.4,
                "pitch": 0.0, "yaw": 0.0, "roll": 0.0,
                "video_writer": back_writer, "video_save_path": back_save_path,
            },
            "top_camera": {
                "width": 1920, "height": 1080, "fov": 110,
                "x": 1.5, "y": 0.0, "z": 8.0,
                "pitch": -90.0, "yaw": 0.0, "roll": 0.0,
                "video_writer": top_writer, "video_save_path": top_save_path
            },
        }
        ## step3: define the camera listener
        self.camera_info["front_camera"]["listen"] = lambda carla_img: self._front_listener(carla_img)
        self.camera_info["back_camera"]["listen"] = lambda carla_img: self._back_listener(carla_img)
        self.camera_info["top_camera"]["listen"] = lambda carla_img: self._top_listener(carla_img)

    def _load_billboard_info(self):
        # TODO: use configuration file to read/write in the future

        self.billboard_box = Box2D(
            top_left=Point(coord=WorldCoordinate(*[-6.9, 166.1, 4.9])),
            top_right=Point(coord=WorldCoordinate(*[-10.1, 166.1, 4.9])),
            bottom_right=Point(coord=WorldCoordinate(*[-10.1, 166.1, 2.5])),
            bottom_left=Point(coord=WorldCoordinate(*[-6.9, 166.1, 2.5])),
        )

    def _listener(self, carla_img, camera):
        bgr_img = get_raw_image(carla_img)
        if camera == "front_camera":  # put into queue for adversarial attack in the next
            put_image_to_queue(self.camera_info[camera]["queue"], bgr_img)

        save_video_frame(self.camera_info[camera]["video_writer"], frame=bgr_img)
        show_image(bgr_img, window_name=camera, width=240, height=135)

    def _front_listener(self, carla_img):
        self._listener(carla_img, camera="front_camera")

    def _back_listener(self, carla_img):
        self._listener(carla_img, camera="back_camera")

    def _top_listener(self, carla_img):
        self._listener(carla_img, camera="top_camera")

    def _close_others(self):
        ## step1: release all the video writers
        for camera in self.camera_info:
            info = self.camera_info[camera]
            if "video_writer" in info:
                info["video_writer"].release()

    def run(self):
        ## step0: hold on for 1.5 secs to let the world run a while
        self._hold_on()

        ## step1: physical-continuous loop attack
        self.conti_loop.loop()

    def _hold_on(self):
        self.tick(times=30, sleep=0.05)

    def scene_retrieve(self):
        ## step0: retrieve image from queue
        bgr_img = get_image_from_queue(
            self.actor_map["front_camera"]["queue"]
        )
        ## step1: crop image to fit the model input
        bgr_img = bgr_img[0:200][75:75 + 66]
        ## step2: from bgr image to nrgb
        return img_transfer(bgr_img, fro="bgr", to="nrgb")

    def get_ego_actor(self):
        return self.actor_map["ego"]


if __name__ == "__main__":
    ## step0: set calra package root path and the world(town)'s name in carla
    carla_root = '../../resources/packages/carla'
    ref_path_file = '../../resources/paths/path.txt'
    world_name = WorldName.town_02.value
    version = CarlaVersion.v_0_9_6.value

    ## step1: construct the self-defined derived carla environment
    # to initialze the world, weather, traffic flow, actors, ego vehicle, etc
    env = HijackCarlaEnv(root=carla_root, world_name=world_name,
                            version=version, ref_path_file=ref_path_file)
    ## step2: run the environment according to your own task
    env.run()
    ## step3: close the environment according to the resources used in the task
    env.close()
