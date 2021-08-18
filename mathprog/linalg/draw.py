## Modified from Math for Programmers
## https://github.com/orlandpm/Math-for-Programmers

from dataclasses import dataclass
from enum import Enum
from math import ceil, floor, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import xlim, ylim


class Color(Enum):
    BLUE = "C0"
    BLACK = "k"
    RED = "C3"
    GREEN = "C2"
    PURPLE = "C4"
    ORANGE = "C2"
    GRAY = "gray"


@dataclass
class Polygon:
    vertices: list[tuple]
    color: Color = Color.BLUE
    fill: bool = False
    alpha: float = 0.4


@dataclass
class Points:
    vectors: list[tuple]
    color: Color = Color.BLACK


@dataclass
class Arrow:
    tip: tuple
    tail: tuple = (0, 0)
    color: Color = Color.RED


@dataclass
class Segment:
    start_point: tuple
    end_point: tuple
    color: Color = Color.BLUE


# Helper function to extract all the vectors from a list of objects
def extract_vectors(objects):
    for object in objects:
        if isinstance(object, Polygon):
            for v in object.vertices:
                yield v
        elif isinstance(object, Points):
            for v in object.vectors:
                yield v
        elif isinstance(object, Arrow):
            yield object.tip
            yield object.tail
        elif isinstance(object, Segment):
            yield object.start_point
            yield object.end_point
        else:
            raise TypeError(f"Unrecognized object: {object}")


def draw(
    *objects, origin=True, axes=True, grid=(1, 1), nice_aspect_ratio=True, width=6, save_as=None
):

    all_vectors = list(extract_vectors(objects))
    xs, ys = zip(*all_vectors)

    max_x, max_y, min_x, min_y = max(0, *xs), max(0, *ys), min(0, *xs), min(0, *ys)

    # Sizing
    if grid:
        x_padding = max(ceil(0.05 * (max_x - min_x)), grid[0])
        y_padding = max(ceil(0.05 * (max_y - min_y)), grid[1])

        plt.xlim(
            floor((min_x - x_padding) / grid[0]) * grid[0],
            ceil((max_x + x_padding) / grid[0]) * grid[0],
        )
        plt.ylim(
            floor((min_y - y_padding) / grid[1]) * grid[1],
            ceil((max_y + y_padding) / grid[1]) * grid[1],
        )

    if origin:
        plt.scatter([0], [0], color=Color.BLACK.value, marker="x")

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2, color=Color.BLACK.value)
        plt.gca().axvline(linewidth=2, color=Color.BLACK.value)

    for object in objects:
        if isinstance(object, Polygon):
            for i in range(0, len(object.vertices)):
                x1, y1 = object.vertices[i]
                x2, y2 = object.vertices[(i + 1) % len(object.vertices)]
                plt.plot([x1, x2], [y1, y2], color=object.color.value)
            if object.fill:
                xs = [v[0] for v in object.vertices]
                ys = [v[1] for v in object.vertices]
                plt.gca().fill(xs, ys, object.fill, alpha=object.alpha)
        elif isinstance(object, Points):
            xs = [v[0] for v in object.vectors]
            ys = [v[1] for v in object.vectors]
            plt.scatter(xs, ys, color=object.color.value)
        elif isinstance(object, Arrow):
            tip, tail = object.tip, object.tail
            tip_length = (xlim()[1] - xlim()[0]) / 20.0
            length = sqrt((tip[1] - tail[1]) ** 2 + (tip[0] - tail[0]) ** 2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(
                tail[0],
                tail[1],
                new_x,
                new_y,
                head_width=tip_length / 1.5,
                head_length=tip_length,
                fc=object.color.value,
                ec=object.color.value,
            )
        elif isinstance(object, Segment):
            x1, y1 = object.start_point
            x2, y2 = object.end_point
            plt.plot([x1, x2], [y1, y2], color=object.color.value)
        else:
            raise TypeError(f"Unrecognized object: {object}")

    fig = plt.gcf()

    if nice_aspect_ratio:
        coords_height = ylim()[1] - ylim()[0]
        coords_width = xlim()[1] - xlim()[0]
        fig.set_size_inches(width, width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()
