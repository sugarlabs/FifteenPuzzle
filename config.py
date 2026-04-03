# This file is part of the Fifteen Puzzle game.
# Copyright (C) 2026 Bishoy Wadea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pygame as pg

# Declare some constants and variables
FPS = 45
WHITE = pg.Color("#DDDDDD")
BLACK = pg.Color("#1A1A1A")
GREY = pg.Color("#333333")
ORANGE = pg.Color("#FF6600")
RED = pg.Color("#FF1F00")

# 15 Puzzle specific settings
BOARD_SIZE = 480
TILE_SIZE = BOARD_SIZE // 4
LINE_WIDTH = 6
CIRCLE_RADIUS = 8
CIRCLE_WIDTH = 2
FRAME_GAP = 80  
GRID_ROWS = 4        
GRID_COLS = 4 

def init():
    global WIN, WIDTH, HEIGHT
    WIN = pg.display.get_surface()
    WIDTH, HEIGHT = WIN.get_size()