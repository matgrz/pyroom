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

single_angle1 = [350]
single_angle2 = [100]
result_single_angle = [[3.4, 3.4]]

# test_angular_distance_calculation variables
angle1 = 30
angle2 = 75
result = math.pi * 45 / 180

# test_decimation variables
hist = {500: 2, 550: 3, 600: 4, 700: 4, 750: 3, 800: 1, 850: 8, 900: 9}
expected_dec_hist = [5, 8, 4, 17]
expected_dec_hist_by_one = [2, 3, 4, 4, 3, 1, 8, 9]

# euclidean test variables
x1 = [5, 5, 5, 5, 5]
x2 = [4, 3, 3, 0, 5]
x3 = [0, 0, 0, 0, 0]
result_x1_x1 = 0
result_x1_x2 = 1.36 / 5
result_x1_x3 = 1

# sort dict variables
dict_to_sort = {"a": 3, "b": 1, "c": 2}
dict_sorted = [('b', 1), ('c', 2), ('a', 3)]

# test_is_estimation_close_enough
real_loc = [1., 1.]
est_loc = [2., 2.]
max_r = pow(2, 0.5)


class ProcessingTest(unittest.TestCase):
    def test_given_mics_and_sources_in_the_corners(self):
        array_of_positions = processing.find_intersections(angle_array1, angle_array2, mic_center1,
                                                           mic_center2)
        log.INFO("array position: ", array_of_positions)
        self.assertTrue(expected_result == array_of_positions, "Positions not equal")

    def test_intersection_of_two_angles(self):
        position = processing.find_intersections(single_angle1, single_angle2, mic_center1, mic_center2)
        log.INFO("array position: ", position)
        self.assertTrue(position == result_single_angle, "Positions not equal")

    def test_angular_distance_calculation(self):
        self.assertAlmostEqual(processing.calculate_angular_distance(angle1, angle2), result)

    def test_decimation(self):
        self.assertEqual(processing.decimate_histogram(hist_data=hist, d=2), expected_dec_hist)

    def test_decimation_by_one(self):
        self.assertEqual(processing.decimate_histogram(hist_data=hist, d=1), expected_dec_hist_by_one)

    def test_euclidean_dist_empty(self):
        self.assertEqual(processing.euclidean_distance(x1, x1), result_x1_x1)

    def test_euclidean_dist(self):
        self.assertAlmostEqual(processing.euclidean_distance(x1, x2), result_x1_x2)

    def test_euclidean_dist_max_difference(self):
        self.assertAlmostEqual(processing.euclidean_distance(x1, x3), result_x1_x3)

    def test_dictionary_sorting(self):
        self.assertEqual(processing.sort_dict_by_value(dict_to_sort), dict_sorted)

    def test_is_estimation_close_enough(self):
        self.assertTrue(processing.is_estimation_close_enough(real_loc, est_loc, max_r))


if __name__ == '__main__':
    unittest.main()
