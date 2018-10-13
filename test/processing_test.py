import unittest
from utils import processing
import math


class ProcessingTest(unittest.TestCase):
    # test_given_mics_and_sources_in_the_corners variables
    angle_array1 = [0, 270]
    angle_array2 = [90, 180]
    mic_center1 = [0, 4]
    mic_center2 = [4, 0]
    expected_result = [[0.0, 4.0], [float('Inf'), None], [None, float('Inf')], [0.0, 0.0]]

    # test_angular_distance_calculation variables

    def test_given_mics_and_sources_in_the_corners(self):
        array_of_positions = processing.find_intersections(self.angle_array1, self.angle_array2, self.mic_center1,
                                                           self.mic_center2)
        print("LOG_INF: ", array_of_positions)
        self.assertTrue(self.expected_result == array_of_positions, "Positions not equal")

    def test_angular_distance_calculation(self):
        self.assertAlmostEqual(processing.calculate_angular_distance(30, 75), math.pi * 45 / 180)


if __name__ == '__main__':
    unittest.main()
