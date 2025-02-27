class RotationType:
    WHD = 0
    HWD = 1
    HDW = 2
    DHW = 3
    DWH = 4
    WDH = 5

    ALL = [WHD, HWD, HDW, DHW, DWH, WDH]
    NOT_UPSIDEDOWN = [WHD, HWD]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2
    # left -> right, bottom -> top, back -> front
    WHD = [WIDTH, HEIGHT, DEPTH]
    # left -> right, back -> front, bottom -> top
    WDH = [WIDTH, DEPTH, HEIGHT]
    # bottom -> top, left -> right, back -> front
    HWD = [HEIGHT, WIDTH, DEPTH]


class Type:
    CUBE = 'cube'
    CYLINDER = 'cylinder'


START_POSITION = [0, 0, 0]
