import numpy as np
import math


def convert_float_signal_to_int(signal):
    """
    Converts a signal which contains floating point data - floats are being converted to int
    :param signal: input data
    :return: signal containing integers
    """
    return np.int16(signal / np.max(np.abs(signal)) * 32767)


def find_intersections(angle_array1, angle_array2, mic_center1, mic_center2):
    """
    Locates all intersections provided by DOA angles.
    :param angle_array1:  array of ints
    :param angle_array2:  array of ints
    :param mic_center1:  [x, y] format ints, central point of microphone array
    :param mic_center2:  [x, y] format ints
    :return: array of [x, y] elements, every element denotes an intersection
    """

    sources_locations = list()

    for angle1 in angle_array1: # kazdy kat z kazdym

        a1 = math.tan(angle1 * math.pi / 180)

        if abs(a1) > 1.0e3:
            b1 = 0.0
        else:
            b1 = round(mic_center1[1] - math.tan(angle1 * math.pi / 180) * mic_center1[0], 4)  # b = y - tg(fi) * x

        for angle2 in angle_array2:
            a2 = math.tan(angle2 * math.pi / 180)
            if abs(a2) > 1.0e3:
                b2 = 0.0
            else:
                b2 = round(mic_center2[1] - a2 * mic_center2[0], 4)

            x = round((b2 - b1) / (a1 - a2), 2)
            y = round(a1 * x + b1, 2)

            if b1 == 0 and b2 == 0 and abs(a1) > 1.0e3 and abs(a2) > 1.0e3:
                sources_locations.append([None, float('Inf')])
            elif abs(x) > 1.0e4 or abs(y) > 1.0e4:
                sources_locations.append([float('Inf'), None])
            else :
                sources_locations.append([x, y])

    return sources_locations


def calculate_angular_distance(x, y):

    x = math.pi * x / 180
    y = math.pi * y / 180
    u_x = [math.cos(x), math.sin(x)]
    u_y = np.transpose([math.cos(y), math.sin(y)])

    return math.acos(np.matmul(u_x, u_y))
