import numpy as np
import math
from utils import log


log = log.Log()


def create_circular_mic_array(center, mics_no, phi, r):
    """
    Creates array with mic_no points located on a circle. It is an imput of pyroomaccoustics mic array.
    The tool provides 2D circular array ony for Beamformer class.
    :param center: center of the circle [x, y, z]
    :param mics_no: number of microphones in the array
    :param phi: counter clockwise rotation of first element (in regard to x-axis)
    :param r: radius of circle
    :return: numpy array of microphones locations
    """
    delta = 2 * np.pi / mics_no
    arr = []

    for i in range(mics_no):
        arr.append([center[0] + r*np.cos(phi+i*delta), center[1] + r*np.sin(phi+i*delta), center[2]])

    mic_arr = [[], [], []]
    for x in range(3):
        row = []
        for y in range(mics_no):
            row.append(round(arr[y][x], 2))
        mic_arr[x] = row.copy()
    return np.array(mic_arr)


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

    for angle1 in angle_array1:

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

    log.INFO("found intersection values: ", sources_locations)
    return sources_locations


def calculate_angular_distance(x, y):
    """
    Calculates angular distance between two angles.
    :param x: first angle [degree]
    :param y: second angle [degree]
    :return: angular distance value [radian]
    """
    x = math.pi * x / 180
    y = math.pi * y / 180
    u_x = [math.cos(x), math.sin(x)]
    u_y = np.transpose([math.cos(y), math.sin(y)])

    try:
        return math.acos(np.matmul(u_x, u_y))
    except:
        log.WRN("LOG_WRN: unexpected error, returning pi")
        return math.pi


def decimate_histogram(hist_data, d):
    """
    Decimates histogram by a decimation factor of d.
    When d == 1 it converts dict histogram to list based histogram.
    :param hist_data: histogram data (dictionary)
    :param d: decimation factor
    :return: list of decimated histogram values by a factor of d
    """
    hist_list = list(hist_data.values())

    h_prim = list()
    for x in range(0, len(hist_list) // d):

        h_prim.append(0)
        for k in range(0, d):
            h_prim[x] += hist_list[d*x + k]

    return h_prim


def euclidean_distance(hist1, hist2):
    """
    Calculates normalized euclidean distance.
    :param hist1: first histogram to be compared
    :param hist2: second histogram to be compared
    :return: euclidean distance [float]
    """
    max_val = max([max(hist1), max(hist2)])
    value = 0
    hist_length = len(hist1)
    for n in range(hist_length):
        value += pow(hist1[n]/max_val - hist2[n]/max_val, 2)

    return value / hist_length


def sort_dict_by_value(dictionary):
    """
    Sorts a dictionary by its values.
    :param dictionary: dictionary to be sorted
    :return: sorted dictionary formatted as a list
    """
    import operator
    return sorted(dictionary.items(), key=operator.itemgetter(1))


def is_estimation_close_enough(estmiated_location, real_location, max_r):
    """
    Verifies whether estimated location is in a range=max_r of real source.
    :param estmiated_location: [x, y] estimated coordinates
    :param real_location: [x, y] real source coordinates
    :param max_r: arbitrary threshold value
    :return: boolean
    """
    d = pow(pow(real_location[0] - estmiated_location[0], 2) + pow(real_location[1] - estmiated_location[1], 2), 0.5)
    log.DBG("calculated distance between real source and estimation = ", d)
    return d <= max_r


def get_matched_angle_indexes(feature_list1, feature_list2, decimation_factor, method_type="EUCLIDEAN"):
    """
    Function calculates euclidean distances and returns indexes of matched directions.
    Index are achieving form sorted dict keys.
    :param feature_list1: single histogram [dictionary]
    :param feature_list2: single histogram [dictionary]
    :param decimation_factor: int
    :param method_type: str, determines which method of histogram matching is used
    :return: array of pairs - every pair contain indexes of matching DOA directions respectively
    """
    feature_list = prepare_decimated_single_feature_list(feature_list1, feature_list2, decimation_factor)

    # D0-0 means comparision between 1st direction from first mic array and 1st indexed direction from second mic array
    euc_result = {}.fromkeys(["D0-0", "D0-1", "D1-0", "D1-1"])  # TODO - implement more civilized matching method

    if method_type == "EUCLIDEAN":
        euc_result["D0-0"] = euclidean_distance(feature_list[0], feature_list[2])
        euc_result["D0-1"] = euclidean_distance(feature_list[0], feature_list[3])
        euc_result["D1-0"] = euclidean_distance(feature_list[1], feature_list[2])
        euc_result["D1-1"] = euclidean_distance(feature_list[1], feature_list[3])
    elif method_type == "PEARSON":
        euc_result["D0-0"] = pearsons_correlation(feature_list[0], feature_list[2])
        euc_result["D0-1"] = pearsons_correlation(feature_list[0], feature_list[3])
        euc_result["D1-0"] = pearsons_correlation(feature_list[1], feature_list[2])
        euc_result["D1-1"] = pearsons_correlation(feature_list[1], feature_list[3])

    sorted_euc = sort_dict_by_value(euc_result)
    return [[int(sorted_euc[0][0][1]), int(sorted_euc[0][0][3])], [int(sorted_euc[1][0][1]), int(sorted_euc[1][0][3])]]


def prepare_decimated_single_feature_list(feature_list1, feature_list2, decimation_factor):
    """
    Prepares signle array of feature lists.
    """
    feature_list = list()
    feature_list.append(decimate_histogram(feature_list1[0], decimation_factor))
    feature_list.append(decimate_histogram(feature_list1[1], decimation_factor))
    feature_list.append(decimate_histogram(feature_list2[0], decimation_factor))
    feature_list.append(decimate_histogram(feature_list2[1], decimation_factor))
    return feature_list


def match_estimations_with_real_sources(angles1, angles2, angle_indexes, config): # TODO - clean this parameter mess
    """
    Predicates whether estimated source is close enough to the real one. [Needs to be rearranged]
    :param angles1:
    :param angles2:
    :param angle_indexes:
    :param config:
    :return: matching verdict [bool]
    """
    max_r = config.max_r
    mics_center1 = config.mic_arr_center1
    mics_center2 = config.mic_arr_center2

    estimation1 = find_intersections([angles1[angle_indexes[0][0]]], [angles2[angle_indexes[0][1]]], mics_center1, mics_center2)
    estimation2 = find_intersections([angles1[angle_indexes[1][0]]], [angles2[angle_indexes[1][1]]], mics_center1, mics_center2)

    log.DBG("estimated location 1: ", estimation1[0])
    log.DBG("estimated location 2: ", estimation2[0])
    log.DBG("real locations: ", config.source_location1)
    log.DBG("real locations: ", config.source_location2)

    # estimation1[0] because finding intersections returns list of pairs(two element lists)
    if is_estimation_close_enough(estimation1[0], config.source_location1, max_r) or is_estimation_close_enough(estimation1[0], config.source_location2, max_r):    # TODO - replace these crappy ifs
        if is_estimation_close_enough(estimation2[0], config.source_location1, max_r) or is_estimation_close_enough(estimation2[0], config.source_location2, max_r):
            return True

    return False


def pearsons_correlation(hist1, hist2):
    """
    Indicates relationships between two histograms.
    :param hist1: list
    :param hist2: list
    :return: D factor
    """
    cov_h1_h2 = np.cov(hist1, hist2)[0][1]
    std_h1 = np.std(hist1)
    std_h2 = np.std(hist2)
    D = (1 - cov_h1_h2 / (std_h1 * std_h2)) / 2
    log.DBG("pearson correlation coeficiency = ", D)
    return D