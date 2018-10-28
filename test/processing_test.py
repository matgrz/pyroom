import unittest
from utils import processing, log
import math


log = log.Log()

# test_given_mics_and_sources_in_the_corners variables
angle_array1 = [0, 270]
angle_array2 = [90, 180]
mic_center1 = [0, 4]
mic_center2 = [4, 0]
expected_result = [[0.0, 4.0], [float('Inf'), None], [None, float('Inf')], [0.0, 0.0]]

# test_angular_distance_calculation variables
angle1 = 30
angle2 = 75
result = math.pi * 45 / 180

# test_decimation variables
hist = [2, 3, 4, 4, 3, 1, 8, 9]
expected_dec_hist = [5, 8, 4, 17]


class ProcessingTest(unittest.TestCase):
    def test_given_mics_and_sources_in_the_corners(self):
        array_of_positions = processing.find_intersections(angle_array1, angle_array2, mic_center1,
                                                           mic_center2)
        print("LOG_INF: ", array_of_positions)
        self.assertTrue(expected_result == array_of_positions, "Positions not equal")

    def test_angular_distance_calculation(self):
        self.assertAlmostEqual(processing.calculate_angular_distance(angle1, angle2), result)

    def test_decimation(self):
        self.assertEqual(processing.decimate_histogram(hist_data=hist, d=2), expected_dec_hist)


if __name__ == '__main__':
    unittest.main()
