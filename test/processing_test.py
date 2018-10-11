import unittest
from utils import processing


class ProcessingTest(unittest.TestCase):

    # test_given_mics_and_sources_in_the_corners variables
    angle_array1 = [0, 270]
    angle_array2 = [90, 180]
    mic_center1 = [0, 4]
    mic_center2 = [4, 0]
    expected_result = [[0.0, 4.0], [float('Inf'), None], [None, float('Inf')], [0.0, 0.0]]

    def test_given_mics_and_sources_in_the_corners(self):

        array_of_positions = processing.find_crossing(self.angle_array1, self.angle_array2, self.mic_center1, self.mic_center2)
        print("LOG_INF: ", array_of_positions)
        self.assertTrue(self.expected_result == array_of_positions, "Positions not equal")


if __name__ == '__main__':
    unittest.main()
