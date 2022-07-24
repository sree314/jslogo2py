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

    def home(self):
        turtle.goto(0, 0)
        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def move(self, distance):
        if distance < 0:
            turtle.backward(-distance)
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

    def setvar(self, varname, value):
        if varname == "led1":
            turtle.leftLED = value != 0
        elif varname == "led2":
            turtle.rightLED = value != 0
        elif varname == "ir1":
            turtle.leftDetector = value != 0
        elif varname == "ir2":
            turtle.rightDetector = value != 0
        elif varname == "emitter":
            turtle.emitter = value != 0
        else:
            pass

    def not_supported(self):
        pass

    def not_implemented(self):
        pass

    def clearscreen(self):
        self.home()

    def clear(self):
        self.not_supported()

    def drawtext(self, text):
        self.not_implemented()

    def fillpath(self, fillcolor):
        self.not_supported()

    def fill(self):
        self.not_supported()

    def arc(self, angle, radius):
        self.not_implemented()

    def getstate(self):
        self.not_supported()

    def setstate(self, state):
        self.not_supported()

    def turtlemode(self, mode):
        self.not_supported()

    def pendown(self, mode):
        if mode:
            turtle.pendown()
        else:
            turtle.penup()

    def color(self, color):
        self.not_implemented()

    def bgcolor(self, color):
        self.not_supported()

    def penwidth(self, width):
        self.not_supported()

    def fontsize(self, size):
        self.not_implemented()

    def fontname(self, name):
        self.not_implemented()

    def position(self, xy):
        turtle.goto(xy[0], xy[1])
        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def heading(self, angle):
        turtle.left(angle)

    def visible(self, visible):
        if not visible:
            # don't know how to make things invisible
            self.not_supported()

    def scrunch(self, sc):
        self.not_implemented()



