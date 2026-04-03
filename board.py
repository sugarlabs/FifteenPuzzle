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
import config
import random
from anim import Animate


class Board:
    def __init__(self, main, center, tile_size=config.TILE_SIZE):
        self.main = main
        self.center = center
        self.tile_size = tile_size
        self.board_size = 4 * tile_size
        
        # Calculate the top-left corner of the board
        self.top_left = (
            center[0] - self.board_size // 2,
            center[1] - self.board_size // 2
        )
        
        # Initialize the grid state (4x4)
        # 0 represents the empty space
        self.grid = self.create_solvable_grid()
        self.empty_pos = self.find_empty_position()
        
        # Create tile animation objects
        self.tiles = []
        self.setup_tiles()
        
        # Create the board border animations
        self.create_border_animations()

    def create_solvable_grid(self):
        """Create a randomly shuffled grid that is guaranteed to be solvable"""
        # Start with solved state
        # grid = [[1, 2, 3, 4], 
        #         [5, 6, 7, 8], 
        #         [9, 10, 11, 12], 
        #         [13, 14, 0, 15]]
        
        # Perform random valid moves to shuffle
        grid = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
        empty_row, empty_col = 3, 3
        moves = 0
        while moves < 200:  # Perform 200 random moves
            # Choose random direction (0=up, 1=right, 2=down, 3=left)
            directions = []
            if empty_row > 0:  # Can move up
                directions.append(0)
            if empty_col < 3:  # Can move right
                directions.append(1)
            if empty_row < 3:  # Can move down
                directions.append(2)
            if empty_col > 0:  # Can move left
                directions.append(3)
                
            direction = random.choice(directions)
            
            # Move tile in the chosen direction
            if direction == 0:  # Up
                grid[empty_row][empty_col] = grid[empty_row-1][empty_col]
                grid[empty_row-1][empty_col] = 0
                empty_row -= 1
            elif direction == 1:  # Right
                grid[empty_row][empty_col] = grid[empty_row][empty_col+1]
                grid[empty_row][empty_col+1] = 0
                empty_col += 1
            elif direction == 2:  # Down
                grid[empty_row][empty_col] = grid[empty_row+1][empty_col]
                grid[empty_row+1][empty_col] = 0
                empty_row += 1
            elif direction == 3:  # Left
                grid[empty_row][empty_col] = grid[empty_row][empty_col-1]
                grid[empty_row][empty_col-1] = 0
                empty_col -= 1
                
            moves += 1
            
        return grid

    def find_empty_position(self):
        """Find the position of the empty tile (value 0)"""
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    return (row, col)
        return (3, 3)  # Default position (should not happen)

    def setup_tiles(self):
        """Create tile objects for each position on the grid"""
        self.tiles = []
        for row in range(4):
            tile_row = []
            for col in range(4):
                value = self.grid[row][col]
                if value > 0:  # Don't create a tile for the empty position
                    tile_x = self.top_left[0] + col * self.tile_size
                    tile_y = self.top_left[1] + row * self.tile_size
                    tile = Tile(self.main, (tile_x, tile_y), value, self.tile_size)
                    tile_row.append(tile)
                else:
                    tile_row.append(None)
            self.tiles.append(tile_row)

    def create_border_animations(self):
        """Create animations for the board border"""
        self.animations = []
        points = [
            (self.top_left[0], self.top_left[1]),
            (self.top_left[0] + self.board_size, self.top_left[1]),
            (self.top_left[0] + self.board_size, self.top_left[1] + self.board_size),
            (self.top_left[0], self.top_left[1] + self.board_size),
        ]
        
        # Create line animations for the border
        for i in range(4):
            start_point = points[i]
            end_point = points[(i + 1) % 4]
            line_anim = Animate(self.main, 700 + i * 100).line(start_point, end_point, config.LINE_WIDTH)
            self.animations.append(line_anim)

    def is_valid_move(self, row, col):
        """Check if the tile at (row, col) can be moved"""
        empty_row, empty_col = self.empty_pos
        
        # A tile can only move if it's adjacent to the empty space
        return (abs(row - empty_row) == 1 and col == empty_col) or \
               (abs(col - empty_col) == 1 and row == empty_row)

    def move_tile(self, row, col):
        """Move the tile at (row, col) to the empty position"""
        if not self.is_valid_move(row, col):
            return False
            
        empty_row, empty_col = self.empty_pos
        
        # Update the grid
        self.grid[empty_row][empty_col] = self.grid[row][col]
        self.grid[row][col] = 0
        
        # Update the empty position
        self.empty_pos = (row, col)
        
        # Move the tile (animate)
        tile = self.tiles[row][col]
        self.tiles[empty_row][empty_col] = tile
        self.tiles[row][col] = None
        
        # Update tile position
        new_x = self.top_left[0] + empty_col * self.tile_size
        new_y = self.top_left[1] + empty_row * self.tile_size
        tile.set_position((new_x, new_y))
        
        # Check if puzzle is solved
        if self.is_solved():
            self.main.solved = True
            
        return True

    def is_solved(self):
        """Check if the puzzle is solved"""
        expect = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:
                    # Last position should be empty
                    if self.grid[row][col] != 0:
                        return False
                else:
                    if self.grid[row][col] != expect:
                        return False
                    expect += 1
        return True

    def handle_click(self, pos):
        """Handle mouse click to move tiles"""
        for row in range(4):
            for col in range(4):
                # Skip the empty position
                if self.grid[row][col] == 0:
                    continue
                    
                # Check if click is on this tile
                tile_x = self.top_left[0] + col * self.tile_size
                tile_y = self.top_left[1] + row * self.tile_size
                tile_rect = pg.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
                
                if tile_rect.collidepoint(pos):
                    return self.move_tile(row, col)
                    
        return False

    def draw(self):
        """Draw the board and all tiles"""
        # Draw board border
        for animation in self.animations:
            animation.update()
            
        # Draw all tiles
        for row in self.tiles:
            for tile in row:
                if tile:
                    tile.draw()


class Tile:
    def __init__(self, main, position, value, size):
        self.main = main
        self.position = position  # (x, y) of top-left corner
        self.value = value
        self.size = size
        self.font = pg.font.Font(None, size // 2)
        self.text = self.font.render(str(value), True, config.WHITE)
        self.text_pos = (
            position[0] + (size - self.text.get_width()) // 2,
            position[1] + (size - self.text.get_height()) // 2
        )
        
        # Create animations for tile border
        self.create_animations()
        
    def create_animations(self):
        """Create animations for the tile border"""
        self.animations = []
        x, y = self.position
        points = [
            (x, y),
            (x + self.size, y),
            (x + self.size, y + self.size),
            (x, y + self.size),
        ]
        
        inner_offset = self.size // 10
        inner_points = [
            (x + inner_offset, y + inner_offset),
            (x + self.size - inner_offset, y + inner_offset),
            (x + self.size - inner_offset, y + self.size - inner_offset),
            (x + inner_offset, y + self.size - inner_offset),
        ]
        
        # Create outer border
        for i in range(4):
            start_point = points[i]
            end_point = points[(i + 1) % 4]
            line_anim = Animate(self.main, color=config.ORANGE).line(start_point, end_point, config.LINE_WIDTH // 2)
            self.animations.append(line_anim)
            
        # Create inner border
        for i in range(4):
            start_point = inner_points[i]
            end_point = inner_points[(i + 1) % 4]
            line_anim = Animate(self.main, color=config.RED).line(start_point, end_point, config.LINE_WIDTH // 3)
            self.animations.append(line_anim)
    
    def set_position(self, new_position):
        """Update tile position (for animation)"""
        self.position = new_position
        self.text_pos = (
            new_position[0] + (self.size - self.text.get_width()) // 2,
            new_position[1] + (self.size - self.text.get_height()) // 2
        )
        
        # Update animations with new position
        self.create_animations()
    
    def draw(self):
        """Draw the tile"""
        # Draw tile background
        pg.draw.rect(
            config.WIN,
            config.GREY,
            pg.Rect(self.position[0], self.position[1], self.size, self.size)
        )
        
        # Draw animations
        for animation in self.animations:
            animation.update(skip=True)  # Skip animation for immediate display
            
        # Draw number
        config.WIN.blit(self.text, self.text_pos)