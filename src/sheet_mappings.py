from enum import Enum

class SheetCol(Enum):
    id = "A"
    name = "B"
    played = "C"
    start = "D"
    end = "E"
    eltime = "F"
    elnettime = "G"
    link = "H"
    statheaders = "I"
    statvals = "J"
    outer_map_table = "I"

class SheetCell(Enum):
    now = "J3"
    paused_map_end = "J25"
    paused_map_start = "I25"
    paused_map_elapsed = "J23"
    activemap = "J26"