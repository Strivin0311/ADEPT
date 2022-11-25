# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================
from adept.envs.carla import get_blueprint, get_color, get_transform


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def set_weather(world, weather_name):
    world.set_weather(
        getattr(carla.WeatherParameters,
                weather_name)
    )


def set_spectator(world, transform, **kwargs):
    transform = get_transform(world=world, mode=transform, **kwargs)
    spectator = world.get_spectator()
    if transform is not None:
        spectator.set_transform(transform)


def apply_control(vehicle, control_input):
    import carla
    control = carla.VehicleControl()
    control.steer, control.throttle, control.brake = \
        control_input["s"], control_input["t"], control_input["b"]
    control.manual_gear_shift = False

    vehicle.apply_control(control)


def add_actor(world, key, mode="filter", choose="random", transform="random",
              color=None, specific_attrs=dict, attach_to=None, listen=None, **kwargs):
    bp = get_blueprint(world=world, key=key, mode=mode, choose=choose, **kwargs)
    if bp is None:
        return None

    color = get_color(blueprint=bp, mode=color, **kwargs)
    if color is not None:
        bp.set_attribute('color', color)

    if specific_attrs is not None \
            and isinstance(specific_attrs, dict) and len(specific_attrs) > 0:
        for attr in specific_attrs:
            if bp.has_attribute(attr) \
                    and bp.get_attribute(attr).is_modifiable:
                bp.set_attribute(attr, specific_attrs[attr])

    transform = get_transform(world=world, mode=transform, **kwargs)
    if transform is None:
        return None

    if attach_to is None:
        return world.spawn_actor(bp, transform)

    actor = world.spawn_actor(bp, transform, attach_to=attach_to)

    if listen is not None \
            and isinstance(listen, type(lambda x: x + 1)):
        actor.listen(listen)

    return actor
