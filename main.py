import numpy as np

from simulationtools import room
from utils import processing
from utils import plotting


#==================================================#
mic_location1 = np.c_[
    [1.00, 4.02, 1.5],   # mic1
    [1.00, 3.98, 1.5],   # mic2
    [1.04, 4.02, 1.5],   # mic3
    [1.04, 3.98, 1.5],   # mic4
    ]

mic_location2 = np.c_[
    [4.02, 1.54, 1.5],   # mic1
    [4.02, 1.50, 1.5],   # mic2
    [3.98, 1.50, 1.5],   # mic3
    [3.98, 1.54, 1.5],   # mic4
    ]

source_location1 = [2.6, 5.7, 1.8]
source_location2 = [2.0, 1.5, 1.8]

angle_from_first_pair = room.receive_angles(mic_location1, source_location1, source_location2)
angle_from_second_pair = room.receive_angles(mic_location2, source_location1, source_location2)

found_crossings = processing.find_intersections(angle_from_first_pair, angle_from_second_pair, [1.02, 4.0], [4.0, 1.52])
print(found_crossings)

plotting.plot_crossings(found_crossings, [source_location1, source_location2], [6., 8., 3.5], [[1.02, 4.], [4., 1.52]],
                        [angle_from_first_pair, angle_from_second_pair])
