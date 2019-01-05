import numpy as np
from simulationtools import room_wrapper
from simulationtools.config import xlsx_parser as parser
from utils import processing
from utils import plotting
from utils import log
import traceback
import sys

log = log.Log()

def get_input_config_file():
    return parser.parse_config(sys.argv[1])

def get_simulation_count():
    first_test = 0
    return len(configs) * configs[first_test].frame_limit / configs[first_test].history_length

def run_single_simulation():
    log.INFO("Simulation for config number ", index)
    room = room_wrapper.RoomWrapper(config)
    angle_from_first_pair = room.receive_angles(config.mic_location1)
    angle_from_second_pair = room.receive_angles(config.mic_location2)
    found_crossings = processing.find_intersections(angle_from_first_pair, angle_from_second_pair,
                                                    config.source_center1[0:2], config.source_center2[0:2])
    if config.plot_intersections:
        plotting.plot_crossings(found_crossings, [config.source_location1, config.source_location2],
                                config.room_dimension, [config.source_center1[0:2], config.source_center2[0:2]],
                                [angle_from_first_pair, angle_from_second_pair])
    if config.calculate_features:
        all_feature_lists1 = room.receive_features(config.mic_location1, angle_from_first_pair)
        all_feature_lists2 = room.receive_features(config.mic_location2, angle_from_second_pair)
        log.INFO("shape of all features lists: ", np.shape(all_feature_lists1))

        for frame_index in range(np.shape(all_feature_lists1)[0]):
            matched_indexes = processing.get_matched_angle_indexes(all_feature_lists1[frame_index],
                                                                   all_feature_lists2[frame_index],
                                                                   config.decimation_factor, config.matching_method)
            result = processing.match_estimations_with_real_sources(angle_from_first_pair, angle_from_second_pair,
                                                                    matched_indexes, config)
            log.INFO("test verdict: ", result)

            if config.plot_histograms:
                plotting.plot_histograms(all_feature_lists1[frame_index], all_feature_lists2[frame_index],
                                         config.decimation_factor, matched_indexes)

            if result:
                return True

    return False


if __name__ == '__main__':
    test_score = 0
    configs = get_input_config_file()
    max_score = get_simulation_count()

    for config, index in zip(configs, range(len(configs))):
        try:
            test_score += run_single_simulation()
        except:
            log.ERR("unexpected error for cfg number " + str(index) + ", error: " + str(traceback.format_exc()))

    log.INFO("Simulation finished")
    log.INFO("Test score: " + str(test_score) + " / " + str(max_score))
