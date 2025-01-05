from .constants import Axis
from .item import Item


def rect_intersect(item1: Item, item2: Item, x: int, y: int):
    """
    Check if two items intersect on a given plane.

    Args:
        item1 (Item): The first item.
        item2 (Item): The second item.
        x (int): The x-axis index.
        y (int): The y-axis index.

    Returns:
        bool: True if the items intersect, False otherwise.
    """
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x] / 2
    cy1 = item1.position[y] + d1[y] / 2
    cx2 = item2.position[x] + d2[x] / 2
    cy2 = item2.position[y] + d2[y] / 2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x] + d2[x]) / 2 and iy < (d1[y] + d2[y]) / 2


def rect_overlap(x1, y1, w1, d1, x2, y2, w2, d2):
    """
    Check if two rectangles overlap in a 2D plane.

    Args:
        x1 (float): X-coordinate of the first rectangle's top-left corner.
        y1 (float): Y-coordinate of the first rectangle's top-left corner.
        w1 (float): Width of the first rectangle.
        d1 (float): Height of the first rectangle.
        x2 (float): X-coordinate of the second rectangle's top-left corner.
        y2 (float): Y-coordinate of the second rectangle's top-left corner.
        w2 (float): Width of the second rectangle.
        d2 (float): Height of the second rectangle.

    Returns:
        bool: True if the rectangles overlap, False otherwise.
    """
    return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + d2 and
            y1 + d1 > y2
    )


def intersect(item1: Item, item2: Item):
    """
    Check if two items intersect in all three dimensions.

    Args:
        item1 (Item): The first item.
        item2 (Item): The second item.

    Returns:
        bool: True if the items intersect in all dimensions, False otherwise.
    """
    return all([
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT),
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH),
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)]
    )
