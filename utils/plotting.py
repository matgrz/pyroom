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

    plt.xlabel("oś x [m]")
    plt.ylabel("oś y [m]")
    # plt.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95))
    plt.show()


def plot_histograms(all_feature_lists1, all_feature_lists2, decimation_factor, matched_indexes):

    feature_list = processing.prepare_decimated_single_feature_list(all_feature_lists1,
                                                                    all_feature_lists2, decimation_factor)
    # map charts ot be painted red with matched indexes
    paint_red = [matched_indexes[0][0], matched_indexes[0][1] + 2]

    max_val = np.amax(feature_list)
    plot_index = 0
    for features in feature_list:
        plt.subplot(2, 2, plot_index+1)
        if plot_index == paint_red[0] or plot_index == paint_red[1]:
            plt.bar(range(len(features)), list(features), align='center', color="red")
        else:
            plt.bar(range(len(features)), list(features), align='center')
        plt.xticks(range(0, len(features), 2), range(0, len(features), 2))
        plt.xlabel("indeks częstotliwości")
        plt.ylabel("liczebność dopasowań")
        plt.ylim(top=1.1*max_val)
        plot_index += 1

    plt.show()
