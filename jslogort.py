#!/bin/env python3
#
# CircuitPython Runtime for jslogo graphics commands.
#
# Author: Sreepathi Pai
# Copyright (C) 2022 University of Rochester
#
# Licensed under the MIT License

import turtle
import time

undefined = None
fence = 1

class JSTurtle:
    curx = 0
    cury = 0
    heading = 0

    def position(self, xy):
        pass

    def home(self):
        turtle.goto(0, 0)
        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def turtlemode(self, mode):
        pass

    def pendown(self, mode):
        if mode:
            turtle.pendown()
        else:
            turtle.penup()

    def move(self, distance):
        if distance < 0:
            turtle.backward(distance)
        else:
            turtle.forward(distance)

        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def turn(self, angle):
        # turtle.left handles negative numbers too
        turtle.left(angle)
        self.heading = turtle.heading()

    def wait(self, time):
        # argument time is 1/60 of seconds
        time.sleep(time * 1.0/60.0)
