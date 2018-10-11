import numpy as np
import math


def convert_float_signal_to_int(signal):
    """
    function converts a signal which contains floating point data - floats are being converted to int
    :param signal: input data
    :return: signal containing integers
    """
    return np.int16(signal / np.max(np.abs(signal)) * 32767)


def find_crossing(angle_array1, angle_array2, mic_center1, mic_center2):

    sources_locations = list()

    for angle1 in angle_array1: # kazdy kat z kazdym

        b1 = mic_center1[1] - math.tan(angle1) * mic_center1[0]     # b = y - tg(fi) * x

        for angle2 in angle_array2:
            b2 = mic_center2[1] - math.tan(angle2) * mic_center2[0]

            x = (b2 - b1) / (math.tan(angle1) - math.tan(angle2))
            y = math.tan(angle1) * x + b1
            sources_locations.append([x, y])

    return sources_locations
