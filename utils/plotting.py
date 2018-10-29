from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import math
import numpy as np
from utils import processing, log


log = log.Log()


def plot_crossings(found_crossings, real_sources, room_dimensions, mics_locations, calculated_angles):

    x_val, y_val = zip(*found_crossings)

    fig = plt.figure("Crossings visualization")
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_val, y_val, marker="o", s=200, label="szacowane lokalizacje")
    ax.add_patch(Rectangle((0., 0.), room_dimensions[0], room_dimensions[1], fill=None, alpha=1))

    ax.scatter(real_sources[0][0], real_sources[0][1], marker="x", s=300, c="orange", label="rzeczywiste lokalizacje")
    ax.scatter(real_sources[1][0], real_sources[1][1], marker="x", s=300, c="orange")

    # for mic in mi?cs_locations:
    ax.scatter(*zip(mics_locations[0]), marker="X", s=100, c="gray", label="macierze mikrofonowe")
    ax.scatter(*zip(mics_locations[1]), marker="X", s=100, c="gray")

    # x = np.linspace(0, 1, 10)
    # ax.plot(x, math.tan(295 * math.pi / 180) * (x - mics_locations[0][0]), linestyle="--")
    plt.xlabel("oś x [m]")
    plt.ylabel("oś y [m]")
    plt.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95))
    # for marker, title in zip([["x", "rzeczywiste lokalizacje"], ["o", "szacowane lokalizacje"], ["X", "macierze mikrofonowe"]]):
    #     plt.plot()
    plt.show()


def plot_histograms(all_feature_lists1, all_feature_lists2, decimation_factor):
    for histogram_number in range(np.shape(all_feature_lists1)[0]):
        feature_list = list()
        feature_list.append(processing.decimate_histogram(all_feature_lists1[histogram_number][0], decimation_factor))
        feature_list.append(processing.decimate_histogram(all_feature_lists1[histogram_number][1], decimation_factor))
        feature_list.append(processing.decimate_histogram(all_feature_lists2[histogram_number][0], decimation_factor))
        feature_list.append(processing.decimate_histogram(all_feature_lists2[histogram_number][1], decimation_factor))

        max_val = np.amax(feature_list)
        plot_index = 1
        for features in feature_list:
            plt.subplot(2, 2, plot_index)
            if plot_index == 1 or plot_index == 3:
                plt.bar(range(len(features)), list(features), align='center', color="red")
            else:
                plt.bar(range(len(features)), list(features), align='center')
            plt.xticks(range(0, len(features), 2), range(0, len(features), 2))
            plt.xlabel("indeks częstotliwości")
            plt.ylabel("liczebność dopasowań")
            plt.ylim(top=1.1*max_val)
            plot_index += 1

        plt.show()

        euc_result = {}.fromkeys(["D13", "D14", "D23", "D24"])
        euc_result["D13"] = processing.euclidean_distance(feature_list[0], feature_list[2])
        euc_result["D14"] = processing.euclidean_distance(feature_list[0], feature_list[3])
        euc_result["D23"] = processing.euclidean_distance(feature_list[1], feature_list[2])
        euc_result["D24"] = processing.euclidean_distance(feature_list[1], feature_list[3])

        log.DBG("euc_result = ", euc_result)
        sorted_euc = processing.sort_dict_by_value(euc_result)
        if sorted_euc[0][0] == "D24" or sorted_euc[0][0] == "D13" and sorted_euc[1][0] == "D24" or sorted_euc[1][0] == "D13":
            log.DBG("   verdict: PASSED")
        else:
            log.DBG("   verdict: FAILED")

