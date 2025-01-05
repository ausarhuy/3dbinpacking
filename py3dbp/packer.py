import copy
from collections import Counter

import numpy as np

from .bin import Bin
from .constants import Axis
from .item import Item


class Packer:
    """
        Initializes a new Packer instance.

        Attributes:
            bins (list): List of Bin objects available for packing.
            items (list): List of Item objects to be packed.
            unfit_items (list): List of items that failed to be packed into any bin.
            total_items (int): Total number of items to be packed.
            binding (list): List of binding constraints for item grouping.
    """
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
        self.binding = []

    def add_bin(self, bin: Bin):
        """
        Adds a single bin to the list of bins.
    
        Args:
            bin (Bin): A Bin object to be added.
        """
        self.bins.append(bin)

    def add_bins(self, bins: list[Bin]):
        """
        Adds multiple bins to the list of bins.
    
        Args:
            bins (list[Bin]): A list of Bin objects to be added.
        """
        self.bins.extend(bins)

    def add_item(self, item: Item):
        """
        Adds a single item to the list of items to be packed.

        Args:
            item (Item): An Item object to be added.
        """
        self.items.append(item)
        self.total_items = len(self.items)

    def add_items(self, items: list[Item]):
        """
        Adds multiple items to the list of items to be packed.

        Args:
            items (list[Item]): A list of Item objects to be added.
        """
        self.items.extend(items)
        self.total_items = len(self.items)

    def pack2bin(self, bin: Bin, new_item: Item, fix_point: bool, check_stable: bool, support_surface_ratio: float):
        """
        Packs a single item into the specified bin, considering constraints.
    
        Args:
            bin (Bin): The bin where the item will be packed.
            new_item (Item): The item to be packed.
            fix_point (bool): Whether to fix the item at a specific point in the bin.
            check_stable (bool): Whether to check the stability of the item after packing.
            support_surface_ratio (float): Minimum acceptable support surface ratio for stability.
        """
        fitted = False
        bin.fix_point = fix_point
        bin.check_stable = check_stable
        bin.support_surface_ratio = support_surface_ratio
        # first put item on (0, 0, 0), if corner exist, first add corner in box.
        if bin.corner != 0 and not bin.items:
            corners = bin.add_corners()
            for i, corner in enumerate(corners):
                bin.put_corner(i, corner)

        elif not bin.items:
            if not bin.put_item(new_item, new_item.position):
                bin.unfitted_items.append(new_item)
                return

        for axis in Axis.WHD:
            for item in bin.items:
                w, h, d = item.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [item.position[0] + w, item.position[1], item.position[2]]
                elif axis == Axis.HEIGHT:
                    # prevent stacking non-stackable items
                    pivot = [item.position[0], item.position[1] + h, item.position[2]]
                    if not item.stackable:
                        continue
                elif axis == Axis.DEPTH:
                    pivot = [item.position[0], item.position[1], item.position[2] + d]

                if bin.put_item(new_item, pivot):
                    fitted = True
                    break
            if fitted:
                break
        if not fitted:
            bin.unfitted_items.append(new_item)

    def sort_binding(self):
        """
        Sorts the items based on the specified binding constraints.
    
        This creates groups of items based on the binding list and rearranges unbound items
        to preserve packing efficiency and group integrity.
    
        """
        b, front, back = [], [], []

        # Create lists based on binding
        for group in self.binding:
            b.append([item for item in self.items if item.group in group])

        # Separate items not in any binding group into front and back
        for item in self.items:
            if all(item.group not in binding_group for binding_group in self.binding):
                if len(b[0]) == 0 and item not in front:
                    front.append(item)
                elif item not in front and item not in back:
                    back.append(item)

        # Find the minimum length of lists in b for balanced sorting
        min_c = min(len(group) for group in b if group)

        # Create sort_bind by interleaving elements from each list up to min_c
        sort_bind = [b[j][i] for i in range(min_c) for j in range(len(b)) if i < len(b[j])]

        # Identify unfit items in a single pass
        sort_bind_set = set(sort_bind)
        self.unfit_items.extend(item for group in b for item in group if item not in sort_bind_set)

        # Concatenate the lists for the final sorted order
        self.items = front + sort_bind + back

    def put_order(self):
        """
        Arranges the order of items within each bin based on the bin's packing type.
    
        Order strategies differ for open-top containers versus general containers.
    
        """
        for bin in self.bins:
            # general container
            if bin.put_type == 1:
                bin.items.sort(key=lambda item: item.position[1], reverse=False)
                bin.items.sort(key=lambda item: item.position[2], reverse=False)
                bin.items.sort(key=lambda item: item.position[0], reverse=False)
            # open-top container
            elif bin.put_type == 2:
                bin.items.sort(key=lambda item: item.position[0], reverse=False)
                bin.items.sort(key=lambda item: item.position[1], reverse=False)
                bin.items.sort(key=lambda item: item.position[2], reverse=False)
        return

    def gravity_center(self, bin: Bin):
        """
        Calculates the deviation of the cargo's gravitational center within the bin.
    
        Args:
            bin (Bin): A Bin object containing packed items.
    
        Returns:
            list: A list of percentages representing the weight distribution in four quadrants.
        """
        w = int(bin.width)
        h = int(bin.height)
        d = int(bin.depth)

        area1 = [set(range(0, w // 2 + 1)), set(range(0, h // 2 + 1)), 0]
        area2 = [set(range(w // 2 + 1, w + 1)), set(range(0, h // 2 + 1)), 0]
        area3 = [set(range(0, w // 2 + 1)), set(range(h // 2 + 1, h + 1)), 0]
        area4 = [set(range(w // 2 + 1, w + 1)), set(range(h // 2 + 1, h + 1)), 0]
        area = [area1, area2, area3, area4]

        for item in bin.items:

            x_st = int(item.position[0])
            y_st = int(item.position[1])
            if item.rotation == 0:
                x_ed = int(item.position[0] + item.width)
                y_ed = int(item.position[1] + item.height)
            elif item.rotation == 1:
                x_ed = int(item.position[0] + item.height)
                y_ed = int(item.position[1] + item.width)
            elif item.rotation == 2:
                x_ed = int(item.position[0] + item.height)
                y_ed = int(item.position[1] + item.depth)
            elif item.rotation == 3:
                x_ed = int(item.position[0] + item.depth)
                y_ed = int(item.position[1] + item.height)
            elif item.rotation == 4:
                x_ed = int(item.position[0] + item.depth)
                y_ed = int(item.position[1] + item.width)
            elif item.rotation == 5:
                x_ed = int(item.position[0] + item.width)
                y_ed = int(item.position[1] + item.depth)

            x_set = set(range(x_st, int(x_ed) + 1))
            y_set = set(range(y_st, y_ed + 1))

            # cal gravity distribution
            for j in range(len(area)):
                if x_set.issubset(area[j][0]) and y_set.issubset(area[j][1]):
                    area[j][2] += int(item.weight)
                    break
                # include x and !include y
                elif x_set.issubset(area[j][0]) == True and y_set.issubset(area[j][1]) == False and len(
                        y_set & area[j][1]) != 0:
                    y = len(y_set & area[j][1]) / (y_ed - y_st) * int(item.weight)
                    area[j][2] += y
                    if j >= 2:
                        area[j - 2][2] += (int(item.weight) - x)
                    else:
                        area[j + 2][2] += (int(item.weight) - y)
                    break
                # include y and !include x
                elif x_set.issubset(area[j][0]) == False and y_set.issubset(area[j][1]) == True and len(
                        x_set & area[j][0]) != 0:
                    x = len(x_set & area[j][0]) / (x_ed - x_st) * int(item.weight)
                    area[j][2] += x
                    if j >= 2:
                        area[j - 2][2] += (int(item.weight) - x)
                    else:
                        area[j + 2][2] += (int(item.weight) - x)
                    break
                # !include x and !include y
                elif x_set.issubset(area[j][0]) == False and y_set.issubset(area[j][1]) == False and len(
                        y_set & area[j][1]) != 0 and len(x_set & area[j][0]) != 0:
                    all = (y_ed - y_st) * (x_ed - x_st)
                    y = len(y_set & area[0][1])
                    y_2 = y_ed - y_st - y
                    x = len(x_set & area[0][0])
                    x_2 = x_ed - x_st - x
                    area[0][2] += x * y / all * int(item.weight)
                    area[1][2] += x_2 * y / all * int(item.weight)
                    area[2][2] += x * y_2 / all * int(item.weight)
                    area[3][2] += x_2 * y_2 / all * int(item.weight)
                    break

        r = [area[0][2], area[1][2], area[2][2], area[3][2]]
        sum_r = sum(r)
        if sum_r==0:
            return [0, 0, 0, 0]
        return list(map(lambda x: round(x / sum_r * 100, 2), r))

    def pack(self, bigger_first=False, distribute_items=True, fix_point=True, check_stable=True,
             support_surface_ratio=0.75, binding=None):
        """
        Packs all the items into the available bins using specified strategies.
    
        Args:
            bigger_first (bool): If True, sorts bins and items by volume in descending order.
            distribute_items (bool): If True, distributes items evenly among bins.
            fix_point (bool): If True, fixes items at specific points when packing.
            check_stable (bool): If True, ensures all items are packed stably.
            support_surface_ratio (float): Minimum acceptable surface support ratio.
            binding (list): List of binding constraints for grouped packing.
        """
        if binding is None:
            binding = []

        # add binding attribute
        self.binding = binding
        # Bin : sorted by volume
        self.bins.sort(key=lambda bin: bin.get_volume(), reverse=bigger_first)
        # Divide `self.items` into stackable and unstackable ranges
        stackable_items = [item for item in self.items if item.stackable]
        unstackable_items = [item for item in self.items if not item.stackable]

        # Count the occurrences of each group for stackable and unstackable items
        stackable_counts = Counter(item.group for item in stackable_items)
        unstackable_counts = Counter(item.group for item in unstackable_items)

        # Sort stackable and unstackable items by volume, weight, and the count of their groups
        stackable_items.sort(
            key=lambda item: (item.get_volume(), item.weight, stackable_counts[item.group]), reverse=bigger_first
        )

        unstackable_items.sort(
            key=lambda item: (item.get_volume(), item.weight, unstackable_counts[item.group]), reverse=bigger_first
        )

        # Combine sorted lists
        self.items = stackable_items + unstackable_items

        # sorted by binding
        if binding:
            self.sort_binding()

        for idx, bin in enumerate(self.bins):
            # Pack stackable items first (0 to n)
            for item in self.items:
                self.pack2bin(bin, item, fix_point, check_stable, support_surface_ratio)

            if binding:
                # resorted
                self.items.sort(key=lambda item: item.get_volume(), reverse=bigger_first)
                self.items.sort(key=lambda item: item.loadbear, reverse=True)
                self.items.sort(key=lambda item: item.priority, reverse=False)
                # clear bin
                bin.items = []
                bin.unfitted_items = self.unfit_items
                bin.fit_items = np.array([[0, bin.width, 0, bin.height, 0, 0]])
                # repacking
                for item in self.items:
                    self.pack2bin(bin, item, fix_point, check_stable, support_surface_ratio)

            # Deviation Of Cargo Gravity Center
            self.bins[idx].gravity = self.gravity_center(bin)

            if distribute_items:
                for bitem in bin.items:
                    if bitem.type == 'corner':
                        continue
                    existed_id = bitem.id
                    for item in copy.copy(self.items):
                        if item.id == existed_id:
                            self.items.remove(item)
                            break

        self.unfit_items = self.items
