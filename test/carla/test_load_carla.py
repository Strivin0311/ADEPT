import unittest
from adept.envs.carla import load_carla


class LoadCarlaTestCase(unittest.TestCase):
    def setUp(self):
        self.root1 = '../../resources/packages/carla/'
        self.root2 = '../../resources/packages/carla'
        self.root3 = '../../resources/packages/carla\\'

    def test_load_carla_default(self):
        self.assertTrue(load_carla(root=self.root1, print_path=True))

    def test_load_carla_0_9_6(self):
        self.assertTrue(load_carla(root=self.root2, version='0.9.6', print_path=True))

    def test_load_carla_0_9_13(self):
        self.assertTrue(load_carla(root=self.root3, version='0.9.13', print_path=True))


if __name__ == '__main__':
    unittest.main()
