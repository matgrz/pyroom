from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import math
import numpy as np

def plot_crossings(found_crossings, real_sources, room_dimensions, mics_locations, calculated_angles):

    x_val, y_val = zip(*found_crossings)

    fig = plt.figure("Crossings visualization")
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_val, y_val)
    ax.add_patch(Rectangle((0., 0.), room_dimensions[0], room_dimensions[1], fill=None, alpha=1))

    for source in real_sources:
        ax.scatter(source[0], source[1], marker="P")

    for mic in mics_locations:
        ax.scatter(*zip(mic), marker="x")

    # x = np.linspace(0, 1, 10)
    # ax.plot(x, math.tan(295 * math.pi / 180) * (x - mics_locations[0][0]), linestyle="--")

    plt.show()