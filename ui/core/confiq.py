from enum import Enum

class Colors:
    PRIMARY = "#ffffff"
    CELL_BG_LIGHT = "#f0d9b5"
    CELL_BG_DARK = "#b58863"
    PAWN = "#2ecc71"
    BACKGROUND = "#ecf0f1"

class Constants:    
    CELL_SIZE = 70
    PADDING = 8
    BORDER_WIDTH = 3
    BOARD_WIDTH = 640
    BOARD_HEIGHT = 640

class CellType(Enum):
    LIGHT = "light"
    DARK = "dark"