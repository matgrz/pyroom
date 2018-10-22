import numpy as np

from simulationtools import room_wrapper
from simulationtools.config import baseconfig as cfg
from utils import processing
from utils import plotting
import matplotlib.pyplot as plt


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

config = cfg.BaseConfig()
room = room_wrapper.RoomWrapper(config)

angle_from_first_pair = room.receive_angles(config.mic_location1)
angle_from_second_pair = room.receive_angles(config.mic_location2)

found_crossings = processing.find_intersections(angle_from_first_pair, angle_from_second_pair, [1.02, 4.0], [4.0, 1.52])
print("LOG_DBG: found crossings ", found_crossings)

plotting.plot_crossings(found_crossings, [config.source_location1, config.source_location2],
                        [6., 8., 3.8], [[1.02, 4.], [4., 1.52]],
                        [angle_from_first_pair, angle_from_second_pair])

feature_list1, feature_list2 = room.receive_features(mic_location1, 2, 1.0)
feature_list3, feature_list4 = room.receive_features(mic_location2, 2, 1.0)

plt.subplot(2, 2, 1)
plt.bar(range(len(feature_list1)), list(feature_list1.values()), align='center')
plt.xticks(range(len(feature_list1)), list(feature_list1.keys()))

plt.subplot(2, 2, 2)
plt.bar(range(len(feature_list2)), list(feature_list2.values()), align='center')
plt.xticks(range(len(feature_list2)), list(feature_list2.keys()))

plt.subplot(2, 2, 3)
plt.bar(range(len(feature_list3)), list(feature_list3.values()), align='center')
plt.xticks(range(len(feature_list3)), list(feature_list3.keys()))

plt.subplot(2, 2, 4)
plt.bar(range(len(feature_list4)), list(feature_list4.values()), align='center')
plt.xticks(range(len(feature_list4)), list(feature_list4.keys()))
plt.show()
