"""
This file contains helper functions for the project
"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import atan2, degrees
import urllib.request
from PIL import Image


# functions
def get_tracking_data():
    """
    Function to read in tracking data and return a dataframe
    """

    return pd.read_csv("./data/tracking_data.csv")


def gini_coefficient(x):
    """Compute Gini coefficient of array of values"""
    diffsum = 0
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x) ** 2 * np.mean(x))


def create_football_field(
    linenumbers=True,
    endzones=True,
    highlight_line=False,
    highlight_line_number=50,
    highlighted_name="Line of Scrimmage",
    fifty_is_los=False,
    figsize=(12, 6.33),
):
    """
    Function that plots the football field for viewing plays.
    """

    # credit https://www.kaggle.com/code/robikscube/nfl-big-data-bowl-plotting-player-position/notebook

    rect = patches.Rectangle(
        (0, 0), 120, 53.3, linewidth=0.1, edgecolor="r", facecolor="darkgreen", zorder=0
    )

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot(
        [
            10,
            10,
            10,
            20,
            20,
            30,
            30,
            40,
            40,
            50,
            50,
            60,
            60,
            70,
            70,
            80,
            80,
            90,
            90,
            100,
            100,
            110,
            110,
            120,
            0,
            0,
            120,
            120,
        ],
        [
            0,
            0,
            53.3,
            53.3,
            0,
            0,
            53.3,
            53.3,
            0,
            0,
            53.3,
            53.3,
            0,
            0,
            53.3,
            53.3,
            0,
            0,
            53.3,
            53.3,
            0,
            0,
            53.3,
            53.3,
            53.3,
            0,
            0,
            53.3,
        ],
        color="white",
    )
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color="gold")
        plt.text(62, 50, "<- Player Yardline at Snap", color="gold")
    # Endzones
    if endzones:
        ez1 = patches.Rectangle(
            (0, 0),
            10,
            53.3,
            linewidth=0.1,
            edgecolor="r",
            facecolor="blue",
            alpha=0.2,
            zorder=0,
        )
        ez2 = patches.Rectangle(
            (110, 0),
            120,
            53.3,
            linewidth=0.1,
            edgecolor="r",
            facecolor="blue",
            alpha=0.2,
            zorder=0,
        )
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis("off")
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(
                x,
                5,
                str(numb - 10),
                horizontalalignment="center",
                fontsize=20,  # fontname='Arial',
                color="white",
            )
            plt.text(
                x - 0.95,
                53.3 - 5,
                str(numb - 10),
                horizontalalignment="center",
                fontsize=20,  # fontname='Arial',
                color="white",
                rotation=180,
            )
    if endzones:
        hash_range = range(11, 110)
    else:
        hash_range = range(1, 120)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color="white")
        ax.plot([x, x], [53.0, 52.5], color="white")
        ax.plot([x, x], [22.91, 23.57], color="white")
        ax.plot([x, x], [29.73, 30.39], color="white")

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color="yellow")
        plt.text(hl + 2, 50, "<- {}".format(highlighted_name), color="yellow")
    return fig, ax


def calc_angle(x, y, x1, y1):
    """
    function to calculate angle between two sets of x-y coordinates
    """

    # change in x and y
    dx = x1 - x
    dy = y1 - y

    # calculate angle
    return degrees(atan2(dy, dx))


def draw_table_image(img_url, ax):
    """
    Draws table image
    """
    club_icon = Image.open(urllib.request.urlopen(img_url))
    club_icon.resize((100, 100))
    ax.imshow(club_icon)
    ax.axis("off")
    return ax


class BboxLocator:
    """
    A helper class to locate a bbox in a given axes.
    Will be used in our leaderboards.
    """

    def __init__(self, bbox, transform):
        self._bbox = bbox
        self._transform = transform

    def __call__(self, ax, renderer):
        _bbox = self._transform.transform_bbox(self._bbox)
        return ax.figure.transFigure.inverted().transform_bbox(_bbox)
