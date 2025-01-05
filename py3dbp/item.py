from uuid import uuid4

from .constants import RotationType, START_POSITION, Type


class Item:
    """
    A class to represent an item with various attributes.
    """

    def __init__(self, partno: str, group: str, type: str, whd: tuple[float], weight: float, priority: int,
                 loadbear: int, upsidedown: bool, color: str, stackable: bool = True,
                 rotations: list[RotationType] = None):
        """
        Initializes an Item object with the specified attributes.

        Args:
            partno (str): The part number of the item.
            group (str): The name of the item.
            type (str): The type of the item (e.g., "cube").
            whd (tuple[float]): A tuple representing width (W), height (H), and depth (D).
            weight (float): The weight of the item.
            priority (int): Item's priority.
            loadbear (int): The maximum weight the item can bear.
            upsidedown (bool): Whether the item can be placed upside down (only applicable to 'cube' type).
            color (str): The color of the item.
            stackable (bool): Whether the item can be stacked.
            rotations (list[RotationType]) : A list of rotation types the item can have.
        """
        self.id = uuid4()  # Unique id
        self.partno = partno
        self.group = group
        self.type = type
        self.width = whd[0]
        self.height = whd[1]
        self.depth = whd[2]
        self.weight = weight
        self.priority = priority
        self.loadbear = loadbear
        self.upsidedown = upsidedown if type==Type.CUBE else False
        self.color = color
        self.position = START_POSITION
        self.rotations = RotationType.ALL if rotations is None else rotations
        self.stackable = stackable
        self.rotation = RotationType.WHD  # set default rotation type is WHD

    def __str__(self):
        """
        Returns a string representation of the Item object, including its dimensions,
        weight, position, and volume.

        Returns:
            str: A formatted string representation of the item.
        """
        return "%s(%sx%sx%s, weight: %s) pos(%s) vol(%s)" % (
            self.partno, self.width, self.height, self.depth, self.weight,
            self.position, self.get_volume()
        )
    
    def set_rotations(self, type: str, upsidedown: bool, rotations: list[int]):
        """
        Determines and sets the appropriate rotation types for the item based
        on its type, whether it can be placed upside down, and specified rotations.
    
        Args:
            type (str): The type of the item (e.g., "cube", "cylinder").
            upsidedown (bool): Whether the item can be placed upside down.
            rotations (list[int]): The list of rotations to be set, if provided.
    
        Returns:
            list[int]: The appropriate rotation types for the item.
        """
        
        if type==Type.CYLINDER or not upsidedown:
            return RotationType.NOT_UPSIDEDOWN
        elif rotations is None and upsidedown:
            return RotationType.ALL
        else:
            return rotations
            
    def get_volume(self):
        """
        Calculates the volume of the item, defined as the product of its width,
        height, and depth.

        Returns:
            float: The calculated volume of the item.
        """
        return self.width * self.height * self.depth

    def get_max_area(self):
        """
        Calculates the maximum area of the item's face, determined as the product
        of the two largest dimensions. If the item can be placed upside down,
        the dimensions are reversed accordingly.

        Returns:
            float: The maximum calculated area of the item.
        """
        dimensions = sorted([self.width, self.height, self.depth], reverse=True) if self.upsidedown \
            else [self.width, self.height, self.depth]
        return dimensions[0] * dimensions[1]

    def get_dimension(self, rotation: int = None):
        """
        Retrieves the dimensions of the item based on its current rotation type.
        Rotation type determines how the width, height, and depth are ordered.
        
        Args:
            rotation (Optional[int]): The item's rotation type.
            
        Returns:
            list: A list of dimensions ordered according to the current rotation type.
        """
        if rotation is None:
            rotation = self.rotation

        rotation_kv = {
            RotationType.WHD: [self.width, self.height, self.depth],
            RotationType.HWD: [self.height, self.width, self.depth],
            RotationType.HDW: [self.height, self.depth, self.width],
            RotationType.DHW: [self.depth, self.height, self.width],
            RotationType.DWH: [self.depth, self.width, self.height],
            RotationType.WDH: [self.width, self.depth, self.height]
        }

        return rotation_kv.get(rotation, [])

    def get_whd_order(self, rotation: int = None):
        """
        Retrieves the order of the width, height, and depth dimensions based on
        the current rotation type.
        
        Args:
            rotation (Optional[int]): The item's rotation type.
            
        Returns:
            list: A list of integers representing the order of dimensions.
        """
        if rotation is None:
            rotation = self.rotation

        rotation_order_kv = {
            RotationType.WHD: [0, 1, 2],
            RotationType.HWD: [1, 0, 2],
            RotationType.HDW: [1, 2, 0],
            RotationType.DHW: [2, 1, 0],
            RotationType.DWH: [2, 0, 1],
            RotationType.WDH: [0, 2, 1]
        }

        return rotation_order_kv.get(rotation, [])

    def get_horizontal_dimensions(self):
        """
        Retrieves horizontal rotation types where the largest dimension is
        not interpreted as the vertical (height).

        Returns:
            list: A list of RotationType values representing horizontal orientations.
        """
        max_dim = max(self.width, self.height, self.depth)
        horizontal_rotations = []

        for rotation in self.rotations:
            dims = self.get_dimension(rotation)
            # Largest dimension is not height (middle dimension)
            if dims[1] != max_dim:
                horizontal_rotations.append(rotation)

        return horizontal_rotations

    def get_vertical_dimensions(self):
        """
        Retrieves vertical rotation types where the largest dimension is
        interpreted as the vertical (height).

        Returns:
            list: A list of RotationType values representing vertical orientations.
        """
        max_dim = max(self.width, self.height, self.depth)
        vertical_rotations = []

        for rotation in self.rotations:
            dims = self.get_dimension(rotation)
            # Largest dimension is height (middle dimension)
            if dims[1] == max_dim:
                vertical_rotations.append(rotation)

        return vertical_rotations
