import numpy as np


def convert_float_signal_to_int(signal):
    """
    function converts a signal which contains floating point data - floats are being converted to int
    :param signal: input data
    :return: signal containing integers
    """
    return np.int16(signal / np.max(np.abs(signal)) * 32767)
