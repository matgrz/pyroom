import numpy as np

import room
from utils import processing


#==================================================#
mic_location1 = np.c_[
    [1.00, 4.02, 1.5],   # mic1
    [1.00, 3.98, 1.5],   # mic2
    [1.04, 4.02, 1.5],   # mic3
    [1.04, 3.98, 1.5],   # mic3]
    ]

mic_location2 = np.c_[
    [4.02, 1.54, 1.5],   # mic1
    [4.02, 1.50, 1.5],   # mic2
    [3.98, 1.50, 1.5],   # mic3
    [3.98, 1.54, 1.5],   # mic3
    ]

source_location1 = [2.6, 5.7, 1.8]
source_location2 = [2.0, 1.5, 1.8]

angle_from_first_pair = room.receive_angles(mic_location1, source_location1, source_location2)
angle_from_second_pair = room.receive_angles(mic_location2, source_location1, source_location2)

# print(angle_from_first_pair)
# print(angle_from_second_pair)
print(processing.find_crossing(angle_from_first_pair, angle_from_second_pair, [1.02, 4.0], [4.0, 1.52]))
