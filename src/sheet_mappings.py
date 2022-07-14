from enum import Enum

class SheetCol(Enum):
    id = "A"
    name = "B"
    played = "C"
    start = "D"
    end = "E"
    eltime = "F"
    elnettime = "G"
    statheaders = "H"
    statvals = "I"
    outer_map_table = "H"

class SheetCell(Enum):
    now = "I3"
    paused_map_end = "I25"
    paused_map_start = "H25"
    paused_map_elapsed = "I23"
    activemap = "I26"