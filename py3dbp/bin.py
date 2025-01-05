import copy

import numpy as np

from .auxiliary_methods import intersect, rect_overlap
from .constants import Type
from .item import Item


class Bin:
    """
    A class to represent a bin for packing items.
    """

    def __init__(self, name: str, whd: tuple[float], max_weight: float, corner: int = 0, put_type: int = 1):
        """
        Initializes a Bin object with the specified attributes.

        Args:
            name (str): The name of the bin.
            whd (tuple[float]): A tuple representing width (W), height (H), and depth (D).
            max_weight (float): The maximum weight the bin can hold.
            corner (int, optional): The corner size of the bin. Defaults to 0.
            put_type (int, optional): The type of putting items. Defaults to 1.
        """
        self.name = name
        self.width = whd[0]
        self.height = whd[1]
        self.depth = whd[2]
        self.max_weight = max_weight
        self.corner = corner
        self.items = []
        self.fit_items = np.array([[0, whd[0], 0, whd[1], 0, 0]])
        self.unfitted_items = []
        self.fix_point = False
        self.check_stable = False
        self.support_surface_ratio = 0
        self.put_type = put_type
        self.gravity = []

    def __str__(self):
        """
        Returns a string representation of the Bin object, including its dimensions and volume.

        Returns:
            str: A formatted string representation of the bin.
        """
        return (
            f"{self.name}({self.width}x{self.height}x{self.depth}, "
            f"max_weight:{self.max_weight}) vol({self.get_volume()})"
        )

    def get_volume(self):
        """
        Calculates the volume of the bin.

        Returns:
            float: The calculated volume of the bin.
        """
        return self.width * self.height * self.depth

    def get_total_weight(self):
        """
        Calculates the total weight of the items in the bin.

        Returns:
            float: The total weight of the items in the bin.
        """
        total_weight = sum(item.weight for item in self.items)
        return total_weight

    def put_item(self, item: Item, pivot: list[int, int, int]):
        """
        Attempts to place an item in the bin at the specified pivot point.

        Args:
            item (Item): The item to be placed in the bin.
            pivot (list): The pivot point for placing the item.

        Returns:
            bool: True if the item fits in the bin, False otherwise.
        """

        fit = False
        valid_item_position = item.position
        item.position = pivot

        for rotation in item.rotations:
            item.rotation = rotation
            dimension = item.get_dimension()

            if self._exceed_boundaries(dimension, pivot):
                continue

            fit = True
            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                if self._exceed_weight_limit(item):
                    return False

                if self.fix_point:
                    dimension, pivot = self._adjust_pivot(dimension, pivot)

                    if self. _check_overlap(dimension, pivot, item.stackable):
                        item.position = valid_item_position
                        return False

                    if self.check_stable:
                        if not self._check_stability(dimension, pivot):
                            item.position = valid_item_position
                            return False

                self.fit_items = np.append(
                    self.fit_items,
                    np.array([
                        [pivot[0], pivot[0] + dimension[0],
                         pivot[1], pivot[1] + dimension[1],
                         pivot[2], pivot[2] + dimension[2]]
                    ]),
                    axis=0
                )

                item.position = [
                    pivot[0],
                    pivot[1],
                    pivot[2]
                ]
                if fit:
                    self.items.append(copy.deepcopy(item))

            else:
                item.position = valid_item_position

            return fit

        item.position = valid_item_position
        return fit

    def _exceed_weight_limit(self, item: Item):
        """
        Checks if adding the given item would exceed the bin's weight limit.
    
        Args:
            item (Item): The item to be checked.
    
        Returns:
            bool: True if the item's weight would exceed the weight limit, False otherwise.
        """
        return self.get_total_weight() + item.weight > self.max_weight

    def _exceed_boundaries(self, dimension: list[int, int, int], pivot: list[int, int, int]):
        """
        Checks if the item's dimension exceed the boundaries of the bin.
    
        Args:
            dimension (list[int, int, int]): The width, height, and depth of the item.
            pivot (list[int, int, int]): The x, y, z coordinates of the item's pivot point.
    
        Returns:
            bool: True if any part of the item's dimension exceeds the bin's boundaries, False otherwise.
        """
        return any(
            bound < pivot[idx] + dim
            for bound, idx, dim in zip([self.width, self.height, self.depth], range(3), dimension)
        )

    def _adjust_pivot(self, dimension: list[int, int, int], pivot: list[int, int, int]):
        """
        Adjusts the pivot point based on the dimensions of the item.

        Args:
            dimension (list): The dimensions of the item.
            pivot (list): The pivot point for placing the item.

        Returns:
            tuple: The adjusted dimensions and pivot point.
        """
        for _ in range(3):
            pivot[1] = self.check_height([
                pivot[0], pivot[0] + dimension[0],
                pivot[1], pivot[1] + dimension[1],
                pivot[2], pivot[2] + dimension[2]
            ])
            pivot[0] = self.check_width([
                pivot[0], pivot[0] + dimension[0],
                pivot[1], pivot[1] + dimension[1],
                pivot[2], pivot[2] + dimension[2]
            ])
            pivot[2] = self.check_depth([
                pivot[0], pivot[0] + dimension[0],
                pivot[1], pivot[1] + dimension[1],
                pivot[2], pivot[2] + dimension[2]
            ])
        return dimension, pivot

    def _check_stability(self, dimension: list[int, int, int], pivot: list[int, int, int]):
        """
        Checks the stability of the item at the specified pivot point.

        Args:
            dimension (list): The dimensions of the item.
            pivot (list): The pivot point for placing the item.

        Returns:
            bool: True if the item is stable, False otherwise.
        """
        item_area_lower = dimension[0] * dimension[1]
        support_area_upper = 0
        for fit_item in self.fit_items:
            if pivot[2] == fit_item[5]:
                area = (
                        len(set(range(int(pivot[0]), int(pivot[0] + dimension[0]))) &
                            set(range(int(fit_item[0]), int(fit_item[1])))) *
                        len(set(range(int(pivot[1]), int(pivot[1] + dimension[1]))) &
                            set(range(int(fit_item[2]), int(fit_item[3]))))
                )
                support_area_upper += area

        if support_area_upper / item_area_lower < self.support_surface_ratio:
            return self._check_vertices_support(dimension, pivot)

        return True

    def _check_vertices_support(self, dimension: list[int, int, int], pivot: list[int, int, int]):
        """
        Checks the support of the vertices of the item at the specified pivot point.

        Args:
            dimension (list): The dimensions of the item.
            pivot (list): The pivot point for placing the item.

        Returns:
            bool: True if all vertices are supported, False otherwise.
        """
        four_vertices = [
            [pivot[0], pivot[1]],
            [pivot[0] + dimension[0], pivot[1]],
            [pivot[0], pivot[1] + dimension[1]],
            [pivot[0] + dimension[0], pivot[1] + dimension[1]]
        ]
        c = [False] * 4
        for fit_item in self.fit_items:
            if pivot[2] == fit_item[5]:
                for idx, vertex in enumerate(four_vertices):
                    if (fit_item[0] <= vertex[0] <= fit_item[1]) and (fit_item[2] <= vertex[1] <= fit_item[3]):
                        c[idx] = True
        return all(c)

    def check_depth(self, unfix_point: list):
        """
        Checks the depth of the bin at the specified unfix point.

        Args:
            unfix_point (list): The unfix point for checking the depth.

        Returns:
            float: The adjusted depth.
        """
        z_ = [[0, 0], [float(self.depth), float(self.depth)]]
        for j in self.fit_items:
            x_bottom = set(range(int(j[0]), int(j[1])))
            x_top = set(range(int(unfix_point[0]), int(unfix_point[1])))
            y_bottom = set(range(int(j[2]), int(j[3])))
            y_top = set(range(int(unfix_point[2]), int(unfix_point[3])))
            if x_bottom & x_top and y_bottom & y_top:
                z_.append([float(j[4]), float(j[5])])

        top_depth = unfix_point[5] - unfix_point[4]
        z_ = sorted(z_, key=lambda z_: z_[1])
        for j in range(len(z_) - 1):
            if z_[j + 1][0] - z_[j][1] >= top_depth:
                return z_[j][1]
        return unfix_point[4]

    def check_width(self, unfix_point: list):
        """
        Checks the width of the bin at the specified unfix point.

        Args:
            unfix_point (list): The unfix point for checking the width.

        Returns:
            float: The adjusted width.
        """
        x_ = [[0, 0], [float(self.width), float(self.width)]]
        for j in self.fit_items:
            z_bottom = set(range(int(j[4]), int(j[5])))
            z_top = set(range(int(unfix_point[4]), int(unfix_point[5])))
            y_bottom = set(range(int(j[2]), int(j[3])))
            y_top = set(range(int(unfix_point[2]), int(unfix_point[3])))
            if z_bottom & z_top and y_bottom & y_top:
                x_.append([float(j[0]), float(j[1])])

        top_width = unfix_point[1] - unfix_point[0]
        x_ = sorted(x_, key=lambda x_: x_[1])
        for j in range(len(x_) - 1):
            if x_[j + 1][0] - x_[j][1] >= top_width:
                return x_[j][1]
        return unfix_point[0]

    def check_height(self, unfix_point: list):
        """
        Checks the height of the bin at the specified unfix point.

        Args:
            unfix_point (list): The unfix point for checking the height.

        Returns:
            float: The adjusted height.
        """
        y_ = [[0, 0], [float(self.height), float(self.height)]]
        for j in self.fit_items:
            x_bottom = set(range(int(j[0]), int(j[1])))
            x_top = set(range(int(unfix_point[0]), int(unfix_point[1])))
            z_bottom = set(range(int(j[4]), int(j[5])))
            z_top = set(range(int(unfix_point[4]), int(unfix_point[5])))
            if x_bottom & x_top and z_bottom & z_top:
                y_.append([float(j[2]), float(j[3])])

        top_height = unfix_point[3] - unfix_point[2]
        y_ = sorted(y_, key=lambda y_: y_[1])
        for j in range(len(y_) - 1):
            if y_[j + 1][0] - y_[j][1] >= top_height:
                return y_[j][1]
        return unfix_point[2]

    def add_corners(self) -> list[Item]:
        """
        Adds corners to the bin.

        Returns:
            list: A list of corners.
        """
        if self.corner != 0:
            corner = self.corner
            return [Item(
                partno='corner{}'.format(i),
                group='corner',
                type=Type.CUBE,
                whd=(corner, corner, corner),
                weight=0,
                priority=0,
                stackable=True,
                loadbear=0,
                upsidedown=True,
                color='gray') for i in range(8)]

    def  _check_overlap(self, dimension: tuple[int, int, int], pivot: list[int, int, int], stackable: bool) -> bool:
        """
        Checks if the new item's position overlaps with any existing items in the bin.

        Args:
            dimension (tuple[int, int, int]): The dimensions (width, height, depth) of the new item.
            pivot (list[int, int, int]): The pivot point (x, y, z) for placing the new item.
            stackable (bool): Whether the new item is stackable or not.

        Returns:
            bool: True if there is an overlap, False otherwise.
        """

        x1, y1, z1 = pivot
        w1, h1, d1 = dimension

        for put_item in self.items:
            x2, y2, z2 = put_item.position
            w2, h2, d2 = put_item.get_dimension()

            # Case 1: New item is above put_item and put_item is not stackable
            if not put_item.stackable:  # The current item is unstackable
                if y1 == y2 + h2:  # New item is vertically above put_item
                    if rect_overlap(x1, z1, w1, d1, x2, z2, w2, d2):  # Check X-Z overlap
                        return True

            # Case 2: New item is below or stacked directly on top and is unstackable
            if not stackable:  # New item is unstackable
                if y1 + h1 == y2 or y1 == y2 + h2:  # Below OR directly above
                    if rect_overlap(x1, z1, w1, d1, x2, z2, w2, d2):  # Check X-Z overlap
                        return True

        # No intersections
        return False

    def put_corner(self, index: int, item: Item):
        """
        Places a corner item in the bin.

        Args:
            index (int): The index of the corner position.
            item (Item): The corner item to be placed.
        """
        x = self.width - self.corner
        y = self.height - self.corner
        z = self.depth - self.corner
        pos = [[0, 0, 0], [0, 0, z], [0, y, z], [0, y, 0], [x, y, 0], [x, 0, 0], [x, 0, z], [x, y, z]]
        item.position = pos[index]
        self.items.append(item)

        corner = [float(item.position[0]), float(item.position[0]) + float(self.corner), float(item.position[1]),
                  float(item.position[1]) + float(self.corner), float(item.position[2]),
                  float(item.position[2]) + float(self.corner)]

        self.fit_items = np.append(self.fit_items, np.array([corner]), axis=0)

    def clear_bin(self):
        """
        Clears the items in the bin.
        """
        self.items = []
        self.fit_items = np.array([[0, self.width, 0, self.height, 0, 0]])
