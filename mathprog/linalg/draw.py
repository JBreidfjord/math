## Modified from Math for Programmers
## https://github.com/orlandpm/Math-for-Programmers

from dataclasses import dataclass
from enum import Enum
from math import ceil, floor, sqrt

import matplotlib.pyplot as plt
import numpy as np
from mathprog.linalg import vectors
from matplotlib.cm import get_cmap
from matplotlib.collections import PatchCollection
from matplotlib.colors import Colormap
from matplotlib.patches import FancyArrowPatch, Polygon
from matplotlib.pyplot import xlim, ylim
from mpl_toolkits.mplot3d import proj3d


class Color(Enum):
    BLUE = "C0"
    BLACK = "k"
    RED = "C3"
    GREEN = "C2"
    PURPLE = "C4"
    ORANGE = "C2"
    GRAY = "gray"


# 2D
@dataclass
class Polygon2D:
    vertices: list[tuple]
    color: Color = Color.BLUE
    fill: bool = False
    alpha: float = 0.4


@dataclass
class Points2D:
    vectors: list[tuple]
    color: Color = Color.BLACK


@dataclass
class Arrow2D:
    tip: tuple
    tail: tuple = (0, 0)
    color: Color = Color.RED


@dataclass
class Segment2D:
    start_point: tuple
    end_point: tuple
    color: Color = Color.BLUE


# Helper function to extract all vectors from a list of objects
def extract_vectors(objects):
    for object in objects:
        if isinstance(object, Polygon2D):
            for v in object.vertices:
                yield v
        elif isinstance(object, Points2D):
            for v in object.vectors:
                yield v
        elif isinstance(object, Arrow2D):
            yield object.tip
            yield object.tail
        elif isinstance(object, Segment2D):
            yield object.start_point
            yield object.end_point
        else:
            raise TypeError(f"Unrecognized object: {object}")


def draw(*objects, axes=True, grid=(1, 1), nice_aspect_ratio=True, width=6, save_as=None):

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

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0], plt.xlim()[1], grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0], plt.ylim()[1], grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2)
        plt.gca().axvline(linewidth=2)

    for object in objects:
        if isinstance(object, Polygon2D):
            if object.color:
                for i in range(0, len(object.vertices)):
                    x1, y1 = object.vertices[i]
                    x2, y2 = object.vertices[(i + 1) % len(object.vertices)]
                    plt.plot([x1, x2], [y1, y2], color=object.color.value)
            if object.fill:
                patches = []
                poly = Polygon(object.vertices, True)
                patches.append(poly)
                p = PatchCollection(patches, color=object.fill)
                plt.gca().add_collection(p)
                if object.color is None:
                    for i in range(0, len(object.vertices)):
                        x1, y1 = object.vertices[i]
                        x2, y2 = object.vertices[(i + 1) % len(object.vertices)]
                        plt.plot([x1, x2], [y1, y2], color=object.fill, linewidth=0)
        elif isinstance(object, Points2D):
            xs = [v[0] for v in object.vectors]
            ys = [v[1] for v in object.vectors]
            plt.scatter(xs, ys, color=object.color.value)
        elif isinstance(object, Arrow2D):
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
        elif isinstance(object, Segment2D):
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


# 3D
class FancyArrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


@dataclass
class Polygon3D:
    vertices: list[tuple]
    color: Color = Color.BLUE


@dataclass
class Points3D:
    vectors: list[tuple]
    color: Color = Color.BLACK


@dataclass
class Arrow3D:
    tip: tuple
    tail: tuple = (0, 0, 0)
    color: Color = Color.RED


@dataclass
class Segment3D:
    start_point: tuple
    end_point: tuple
    color: Color = Color.BLUE
    linestyle: str = "solid"


@dataclass
class Box3D:
    vector: tuple


# Helper function to extract all vectors from a list of objects
def extract_vectors_3D(objects):
    for object in objects:
        if isinstance(object, Polygon3D):
            for v in object.vertices:
                yield v
        elif isinstance(object, Points3D):
            for v in object.vectors:
                yield v
        elif isinstance(object, Arrow3D):
            yield object.tip
            yield object.tail
        elif isinstance(object, Segment3D):
            yield object.start_point
            yield object.end_point
        elif isinstance(object, Box3D):
            yield object.vector
        else:
            raise TypeError(f"Unrecognized object: {object}")


def draw3d(
    *objects,
    origin=True,
    axes=True,
    save_as=None,
    azim=None,
    elev=None,
    xlim=None,
    ylim=None,
    zlim=None,
    xticks=None,
    yticks=None,
    zticks=None,
    depthshade=False,
):

    fig = plt.gcf()
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=elev, azim=azim)

    all_vectors = list(extract_vectors_3D(objects))
    if origin:
        all_vectors.append((0, 0, 0))
    xs, ys, zs = zip(*all_vectors)

    max_x, min_x = max(0, *xs), min(0, *xs)
    max_y, min_y = max(0, *ys), min(0, *ys)
    max_z, min_z = max(0, *zs), min(0, *zs)

    x_size = max_x - min_x
    y_size = max_y - min_y
    z_size = max_z - min_z

    padding_x = 0.05 * x_size if x_size else 1
    padding_y = 0.05 * y_size if y_size else 1
    padding_z = 0.05 * z_size if z_size else 1

    plot_x_range = (min(min_x - padding_x, -2), max(max_x + padding_x, 2))
    plot_y_range = (min(min_y - padding_y, -2), max(max_y + padding_y, 2))
    plot_z_range = (min(min_z - padding_z, -2), max(max_z + padding_z, 2))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    def draw_segment(start, end, color=Color.BLACK, linestyle="solid"):
        xs, ys, zs = [[start[i], end[i]] for i in range(0, 3)]
        ax.plot(xs, ys, zs, color.value, linestyle=linestyle)

    if axes:
        draw_segment((plot_x_range[0], 0, 0), (plot_x_range[1], 0, 0))
        draw_segment((0, plot_y_range[0], 0), (0, plot_y_range[1], 0))
        draw_segment((0, 0, plot_z_range[0]), (0, 0, plot_z_range[1]))

    if origin:
        ax.scatter([0], [0], [0], color=Color.BLACK.value, marker="x")

    for object in objects:
        if isinstance(object, Points3D):
            xs, ys, zs = zip(*object.vectors)
            ax.scatter(xs, ys, zs, color=object.color.value, depthshade=depthshade)

        elif isinstance(object, Polygon3D):
            for i in range(0, len(object.vertices)):
                draw_segment(
                    object.vertices[i],
                    object.vertices[(i + 1) % len(object.vertices)],
                    color=object.color,
                )

        elif isinstance(object, Arrow3D):
            xs, ys, zs = zip(object.tail, object.tip)
            a = FancyArrow3D(
                xs, ys, zs, mutation_scale=20, arrowstyle="-|>", color=object.color.value
            )
            ax.add_artist(a)

        elif isinstance(object, Segment3D):
            draw_segment(
                object.start_point,
                object.end_point,
                color=object.color,
                linestyle=object.linestyle,
            )

        elif isinstance(object, Box3D):
            x, y, z = object.vector
            kwargs = {"linestyle": "dashed", "color": Color.GRAY}
            draw_segment((0, y, 0), (x, y, 0), **kwargs)
            draw_segment((0, 0, z), (0, y, z), **kwargs)
            draw_segment((0, 0, z), (x, 0, z), **kwargs)
            draw_segment((0, y, 0), (0, y, z), **kwargs)
            draw_segment((x, 0, 0), (x, y, 0), **kwargs)
            draw_segment((x, 0, 0), (x, 0, z), **kwargs)
            draw_segment((0, y, z), (x, y, z), **kwargs)
            draw_segment((x, 0, z), (x, y, z), **kwargs)
            draw_segment((x, y, 0), (x, y, z), **kwargs)
        else:
            raise TypeError(f"Unrecognized object: {object}")

    if xlim and ylim and zlim:
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        ax.set_zlim(*zlim)
    if xticks and yticks and zticks:
        plt.xticks(xticks)
        plt.yticks(yticks)
        ax.set_zticks(zticks)

    if save_as:
        plt.savefig(save_as)

    plt.show()


# 3D Shape Drawing
def vertices(faces: list):
    return list(set([vertex for face in faces for vertex in face]))


def component(vector: tuple, direction: tuple):
    return vectors.dot(vector, direction) / vectors.length(direction)


def vector_to_2d(vector: tuple):
    return (component(vector, (1, 0, 0)), component(vector, (0, 1, 0)))


def face_to_2d(face: list):
    return [vector_to_2d(vertex) for vertex in face]


def normal(face: list):
    return vectors.cross(vectors.subtract(face[1], face[0]), vectors.subtract(face[2], face[0]))


def render(faces: list, color_map: Colormap = None, light: tuple = (1, 2, 3), lines: Color = None):
    if not isinstance(color_map, Colormap):
        color_map = get_cmap("Blues")

    unit_light = vectors.unit(light)

    polygons = []
    for face in faces:
        # Compute normal vector with length 1
        unit_normal = vectors.unit(normal(face))
        if unit_normal[2] > 0:
            # Calculate shading with dot product
            c = color_map(1 - vectors.dot(unit_normal, unit_light))
            p = Polygon2D(face_to_2d(face), fill=c, color=lines)
            polygons.append(p)

    draw(*polygons, axes=False, grid=None)
