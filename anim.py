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
from math import sqrt
import config


class Animate:

    def LINEAR(x):
        return x

    def EASE_OUT_QUART(x):
        return 1 - pow(1 - x, 4)

    def EASE_IO_QUART(x):
        return 8 * pow(x, 4) if x < 0.5 else 1 - pow(-2 * x + 2, 4) / 2

    def __init__(self, main, dur=500, color=config.WHITE, fn=EASE_OUT_QUART):
        self.main = main
        self.color = color
        self.function = fn
        self.remove = False
        self.dur = dur
        self.start_time = pg.time.get_ticks()
        self.final_time = self.start_time + dur
        self.type = None
        self.sub_animations = None

    def line(self, p1, p2, width=config.LINE_WIDTH):
        self.type = "line"
        self.finished = False
        self.width = width
        self.p1 = pg.Vector2(p1)
        self.p2 = pg.Vector2(p2)
        self.p = self.p2 - self.p1
        self.length = sqrt(self.p.x ** 2 + self.p.y ** 2)
        return self

    def circle(self, center, radius=config.CIRCLE_RADIUS, width=config.CIRCLE_WIDTH):
        self.type = "circle"
        self.finished = False
        self.width = width
        self.radius = radius
        self.r = radius
        self.center = pg.Vector2(center)
        self.rect = pg.Rect(
            (center - pg.Vector2(radius, radius)), (2 * radius, 2 * radius)
        )
        return self

    def rect(self, top_left, size, width=config.LINE_WIDTH):
        self.type = "rect"
        self.finished = False
        self.width = width
        self.top_left = pg.Vector2(top_left)
        self.size = pg.Vector2(size)
        self.lines = [
            Animate(self.main, self.dur, self.color, self.function).line(
                (self.top_left.x, self.top_left.y),
                (self.top_left.x + self.size.x, self.top_left.y),
                width
            ),
            Animate(self.main, self.dur, self.color, self.function).line(
                (self.top_left.x + self.size.x, self.top_left.y),
                (self.top_left.x + self.size.x, self.top_left.y + self.size.y),
                width
            ),
            Animate(self.main, self.dur, self.color, self.function).line(
                (self.top_left.x + self.size.x, self.top_left.y + self.size.y),
                (self.top_left.x, self.top_left.y + self.size.y),
                width
            ),
            Animate(self.main, self.dur, self.color, self.function).line(
                (self.top_left.x, self.top_left.y + self.size.y),
                (self.top_left.x, self.top_left.y),
                width
            )
        ]
        return self

    def setup_remove(self, dur=500):
        self.finished = True
        self.remove = True
        self.dur = dur
        self.start_time = pg.time.get_ticks()
        self.final_time = self.start_time + self.dur
        if self.sub_animations is not None:
            for i in self.sub_animations:
                i.setup_remove(dur)
        if hasattr(self, 'lines'):
            for line in self.lines:
                line.setup_remove(dur)

    def update(self, skip=False):
        # Call method recursively for compound objects
        if self.type == "rect" and hasattr(self, 'lines'):
            for line in self.lines:
                line.update(skip)
            return

        # Calculate the animation
        if not self.finished or self.remove:
            if pg.time.get_ticks() < self.final_time and not skip:
                fraction = (pg.time.get_ticks() - self.start_time) / self.dur
                if fraction < 0.01:
                    fraction += 0.008

                if self.remove:
                    fraction = 1 - fraction

                if self.type == "line":
                    self.p.scale_to_length(
                        self.length * self.function(fraction)
                    )
                elif self.type == "circle":
                    self.r = self.radius - self.width * self.function(fraction)
            else:
                if self.type == "line":
                    self.p = self.p2 - self.p1
                    if self.remove:
                        self.p = pg.Vector2(0, 0)
                if self.type == "circle":
                    self.r = self.radius - self.width
                    if self.remove:
                        self.r = self.radius
                self.remove = False
                self.finished = True

        # Draw stuff
        if self.type == "line":
            pg.draw.line(config.WIN,
                         self.color,
                         self.p1,
                         self.p + self.p1,
                         self.width)
        elif self.type == "circle":
            pg.draw.circle(
                config.WIN,
                self.color,
                (int(self.center.x), int(self.center.y)),
                int(self.radius),
            )
            pg.draw.circle(
                config.WIN,
                config.BLACK,
                (int(self.center.x), int(self.center.y)),
                int(self.r)
            )