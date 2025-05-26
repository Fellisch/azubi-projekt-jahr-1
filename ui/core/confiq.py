from enum import Enum

class Colors:
    PRIMARY = "#FEFAE0"
    SECONDARY = "#D4A373"
    TERTIARY = "#FAEDCD"
    CTA_PRIMARY = "#E9EDC9"
    CTA_HOVER = "#CCD5AE"
    FONT_PRIMARY = "#252422"
    WHITE = "#FDFFFC"
    FIRST_PLAYER = "#FB8500"
    SECOND_PLAYER = "#8ECAE6"

class Constants:    
    CELL_SIZE = 100
    PADDING = 20
    BORDER_WIDTH = 20
    BOARD_WIDTH = 1280
    BOARD_HEIGHT = 820
    CELL_SPACING = 20

class CellType(Enum):
    LIGHT = "light"
    DARK = "dark"