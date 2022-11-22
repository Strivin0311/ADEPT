# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

import glob
import os
import sys


# ==================================================================================================
# -- functions -------------------------------------------------------------------------------------
# ==================================================================================================

def load_carla(root: str, version: str = None, print_path=False):
    """
    load carla environment from an egg file packaged by carla
    :param root: the carla package's directory path
    :param version: the carla version string, such as '0.9.6', '0.9.13', etc [default = latest version: '0.9.13']
    :param print_path: if set True, print the relative path of the carla package to load on the Terminal
    :return: True if load succeeded, otherwise False
    :raise IndexError: the carla egg file can't be loaded
    """
    if version is None:  # load default version
        version = '0.9.13'  # the latest version of carla until 2022.11.8

    # load carla egg package file into system path
    # copied from carla python API
    egg_file_path = os.path.join(root, 'carla-%s-py%d.%d-%s.egg')
    if print_path:
        print('The relative path of the carla package to load is: {}'.format(egg_file_path))

    try:
        sys.path.append(
            glob.glob(egg_file_path %
                      (version,
                       sys.version_info.major,  # major python version: python 3.*
                       sys.version_info.minor,  # minor python version: python *.7
                       'win-amd64' if os.name == 'nt'  # OS version: Windows
                       else 'linux-x86_64'))[0]  # OS version: Linux
        )
    except IndexError as e:
        print("~~the carla egg file to load got something wrong~~", e)
        return False

    return True


def load_client(ip='localhost', port=2000, timeout=10):
    import carla

    client = carla.Client(ip, port)
    client.set_timeout(timeout)

    return client


def load_world(client, world_name, sync=True, delta=0.0):
    world = client.load_world(world_name)

    if sync:  # open the synchronous mode with fixed_delta_seconds = delta
        settings = world.get_settings()
        settings.synchronous_mode = True
        if delta > 0:
            settings.fixed_delta_seconds = delta
        world.apply_settings(settings)

    return world
