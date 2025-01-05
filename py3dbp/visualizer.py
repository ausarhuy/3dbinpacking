import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, Circle

from .constants import Type


class Visualizer:
    """
    A class to visualize 3D bin and the items they contain, using Matplotlib.
    """

    def __init__(self, bin):
        """
        Initializes the Visualizer class with bin attributes.

        Args:
            bin (Bin): An object representing the bin, containing items, width, height, and depth.
        """
        self.items = bin.items
        self.width = bin.width
        self.height = bin.height
        self.depth = bin.depth

    def _plot_cube(self, ax, x, y, z, dx, dy, dz, color='red', linewidth=1, text="", fontsize=15, alpha=0.5, mode=2):
        """
        Plots a 3D cube at the specified position with the given dimensions.

        Args:
            ax (Axes3D): The Matplotlib 3D axis to plot on.
            x, y, z (float): Coordinates of the cube's bottom-left corner.
            dx, dy, dz (float): Dimensions of the cube along x, y, z axes.
            color (str): Color of the cube.
            mode (int): 1 for wireframe, 2 for filled cube.
            linewidth (float): Line width for wireframe mode.
            text (str): Text label inside the cube.
            fontsize (int): Font size of the label.
            alpha (float): Transparency of the cube.
        """
        xx = [x, x, x + dx, x + dx, x]
        yy = [y, y + dy, y + dy, y, y]

        kwargs = {'alpha': 1, 'color': color, 'linewidth': linewidth}
        if mode == 1:
            ax.plot3D(xx, yy, [z] * 5, **kwargs)
            ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
            ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
            ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)
        else:
            p = Rectangle((x, y), dx, dy, fc=color, ec='black', alpha=alpha)
            p2 = Rectangle((x, y), dx, dy, fc=color, ec='black', alpha=alpha)
            p3 = Rectangle((y, z), dy, dz, fc=color, ec='black', alpha=alpha)
            p4 = Rectangle((y, z), dy, dz, fc=color, ec='black', alpha=alpha)
            p5 = Rectangle((x, z), dx, dz, fc=color, ec='black', alpha=alpha)
            p6 = Rectangle((x, z), dx, dz, fc=color, ec='black', alpha=alpha)
            ax.add_patch(p)
            ax.add_patch(p2)
            ax.add_patch(p3)
            ax.add_patch(p4)
            ax.add_patch(p5)
            ax.add_patch(p6)

            if text != "":
                ax.text((x + dx / 2), (y + dy / 2), (z + dz / 2), str(text), color='black', fontsize=fontsize,
                        ha='center', va='center')

            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            art3d.pathpatch_2d_to_3d(p2, z=z + dz, zdir="z")
            art3d.pathpatch_2d_to_3d(p3, z=x, zdir="x")
            art3d.pathpatch_2d_to_3d(p4, z=x + dx, zdir="x")
            art3d.pathpatch_2d_to_3d(p5, z=y, zdir="y")
            art3d.pathpatch_2d_to_3d(p6, z=y + dy, zdir="y")

    def _plot_cylinder(self, ax, x, y, z, dx, dy, dz, color='red', text="", fontsize=10, alpha=0.2):
        """
        Plots a 3D cylinder at the specified position.

        Args:
            ax (Axes3D): The Matplotlib 3D axis to plot on.
            x, y, z (float): Coordinates of the cylinder's bottom-center.
            dx, dy, dz (float): Dimensions of the cylinder along x, y, z axes.
            color (str): Color of the cylinder.
            text (str): Text label inside the cylinder.
            fontsize (int): Font size of the label.
            alpha (float): Transparency of the cylinder.
        """
        p = Circle((x + dx / 2, y + dy / 2), radius=dx / 2, color=color, alpha=0.5)
        p2 = Circle((x + dx / 2, y + dy / 2), radius=dx / 2, color=color, alpha=0.5)
        ax.add_patch(p)
        ax.add_patch(p2)
        art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
        art3d.pathpatch_2d_to_3d(p2, z=z + dz, zdir="z")
        # plot a circle in the middle of the cylinder
        center_z = np.linspace(0, dz, 10)
        theta = np.linspace(0, 2 * np.pi, 10)
        theta_grid, z_grid = np.meshgrid(theta, center_z)
        x_grid = dx / 2 * np.cos(theta_grid) + x + dx / 2
        y_grid = dy / 2 * np.sin(theta_grid) + y + dy / 2
        z_grid = z_grid + z
        ax.plot_surface(x_grid, y_grid, z_grid, shade=False, fc=color, alpha=alpha, color=color)

        if text != "":
            ax.text((x + dx / 2), (y + dy / 2), (z + dz / 2), str(text), color='black', fontsize=fontsize, ha='center',
                    va='center')

    def plot_box_and_items(self, title="", alpha=0.2, write_num=False, fontsize=10):
        """
        Plots the bin and the items it contains in 3D.

        Args:
            title (str): Title of the plot.
            alpha (float): Transparency of the items.
            write_num (bool): Whether to label items with their identifiers.
            fontsize (int): Font size for labels.

        Returns:
            matplotlib.figure.Figure: The Matplotlib figure containing the plot.
        """
        plt.figure()
        ax = plt.axes(projection='3d')

        # plot bin
        self._plot_cube(ax, 0, 0, 0, float(self.width), float(self.height), float(self.depth), color='black',
                        linewidth=1.5, text="", mode=1)

        counter = 0
        # fit rotation type
        for item in self.items:
            x, y, z = item.position
            w, h, d = item.get_dimension()
            color = item.color
            text = item.partno if write_num else ""

            if item.type == Type.CUBE:
                # plot item of cube
                self._plot_cube(ax, float(x), float(y), float(z), float(w), float(h), float(d), color=color, mode=2,
                                text=text, fontsize=fontsize, alpha=alpha)
            elif item.type == Type.CYLINDER:
                # plot item of cylinder
                self._plot_cylinder(ax, float(x), float(y), float(z), float(w), float(h), float(d), color=color,
                                    text=text, fontsize=fontsize, alpha=alpha)

            counter = counter + 1

        plt.title(title)
        self.set_axes_equal(ax)
        return plt

    @staticmethod
    def set_axes_equal(ax: Axes):
        """
        Adjusts the axes of a 3D plot to ensure equal scaling.

        Args:
            ax (Axes): The Matplotlib 3D axis to adjust.
        """
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5 * max([x_range, y_range, z_range])

        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
