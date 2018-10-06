import numpy as np

import room

#==================================================#
# mic_location1 = np.array([[1.0, 1.0], [3.98, 4.02], [1.5, 1.5]])
# mic_location2 = np.array([[3.02, 2.98], [1.5, 1.5], [1.5, 1.5]])
mic_location1 = np.c_[
    [1.0, 4.02, 1.5],   # mic1
    [1.0, 3.98, 1.5],   # mic2
    ]

mic_location2 = np.c_[
    [3.02, 1.5, 1.5],   # mic1
    [2.98, 1.5, 1.5],   # mic2
    ]

source_location1 = [2.6, 4.7, 1.8]
source_location2 = [1.1, 1.5, 1.8]

angle_from_first_pair = room.receive_angles(mic_location1, source_location1, source_location1)
angle_from_second_pair = room.receive_angles(mic_location2, source_location1, source_location1)

print(angle_from_first_pair)
print(angle_from_second_pair)