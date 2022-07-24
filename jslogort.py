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

_CSS_COLORS = {
    "black": (0,0,0), #000000
    "silver": (192,192,192), #C0C0C0
    "gray": (128,128,128), #808080
    "white": (255,255,255), #FFFFFF
    "maroon": (128,0,0), #800000
    "red": (255,0,0), #FF0000
    "purple": (128,0,128), #800080
    "fuchsia": (255,0,255), #FF00FF
    "green": (0,128,0), #008000
    "lime": (0,255,0), #00FF00
    "olive": (128,128,0), #808000
    "yellow": (255,255,0), #FFFF00
    "navy": (0,0,128), #000080
    "blue": (0,0,255), #0000FF
    "teal": (0,128,128), #008080
    "aqua": (), #00FFFF
    "aliceblue": (240,248,255), #f0f8ff
    "antiquewhite": (250,235,215), #faebd7
    "aqua": (0,255,255), #00ffff
    "aquamarine": (127,255,212), #7fffd4
    "azure": (240,255,255), #f0ffff
    "beige": (245,245,220), #f5f5dc
    "bisque": (255,228,196), #ffe4c4
    "black": (0,0,0), #000000
    "blanchedalmond": (255,235,205), #ffebcd
    "blue": (0,0,255), #0000ff
    "blueviolet": (138,43,226), #8a2be2
    "brown": (165,42,42), #a52a2a
    "burlywood": (222,184,135), #deb887
    "cadetblue": (95,158,160), #5f9ea0
    "chartreuse": (127,255,0), #7fff00
    "chocolate": (210,105,30), #d2691e
    "coral": (255,127,80), #ff7f50
    "cornflowerblue": (100,149,237), #6495ed
    "cornsilk": (255,248,220), #fff8dc
    "crimson": (220,20,60), #dc143c
    "cyan": (0,255,255), #00ffff
    "darkblue": (0,0,139), #00008b
    "darkcyan": (0,139,139), #008b8b
    "darkgoldenrod": (184,134,11), #b8860b
    "darkgray": (169,169,169), #a9a9a9
    "darkgreen": (0,100,0), #006400
    "darkgrey": (169,169,169), #a9a9a9
    "darkkhaki": (189,183,107), #bdb76b
    "darkmagenta": (139,0,139), #8b008b
    "darkolivegreen": (85,107,47), #556b2f
    "darkorange": (255,140,0), #ff8c00
    "darkorchid": (153,50,204), #9932cc
    "darkred": (139,0,0), #8b0000
    "darksalmon": (233,150,122), #e9967a
    "darkseagreen": (143,188,143), #8fbc8f
    "darkslateblue": (72,61,139), #483d8b
    "darkslategray": (47,79,79), #2f4f4f
    "darkslategrey": (47,79,79), #2f4f4f
    "darkturquoise": (0,206,209), #00ced1
    "darkviolet": (148,0,211), #9400d3
    "deeppink": (255,20,147), #ff1493
    "deepskyblue": (0,191,255), #00bfff
    "dimgray": (105,105,105), #696969
    "dimgrey": (105,105,105), #696969
    "dodgerblue": (30,144,255), #1e90ff
    "firebrick": (178,34,34), #b22222
    "floralwhite": (255,250,240), #fffaf0
    "forestgreen": (34,139,34), #228b22
    "fuchsia": (255,0,255), #ff00ff
    "gainsboro": (220,220,220), #dcdcdc
    "ghostwhite": (248,248,255), #f8f8ff
    "gold": (255,215,0), #ffd700
    "goldenrod": (218,165,32), #daa520
    "gray": (128,128,128), #808080
    "green": (0,128,0), #008000
    "greenyellow": (173,255,47), #adff2f
    "grey": (128,128,128), #808080
    "honeydew": (240,255,240), #f0fff0
    "hotpink": (255,105,180), #ff69b4
    "indianred": (205,92,92), #cd5c5c
    "indigo": (75,0,130), #4b0082
    "ivory": (255,255,240), #fffff0
    "khaki": (240,230,140), #f0e68c
    "lavender": (230,230,250), #e6e6fa
    "lavenderblush": (255,240,245), #fff0f5
    "lawngreen": (124,252,0), #7cfc00
    "lemonchiffon": (255,250,205), #fffacd
    "lightblue": (173,216,230), #add8e6
    "lightcoral": (240,128,128), #f08080
    "lightcyan": (224,255,255), #e0ffff
    "lightgoldenrodyellow": (250,250,210), #fafad2
    "lightgray": (211,211,211), #d3d3d3
    "lightgreen": (144,238,144), #90ee90
    "lightgrey": (211,211,211), #d3d3d3
    "lightpink": (255,182,193), #ffb6c1
    "lightsalmon": (255,160,122), #ffa07a
    "lightseagreen": (32,178,170), #20b2aa
    "lightskyblue": (135,206,250), #87cefa
    "lightslategray": (119,136,153), #778899
    "lightslategrey": (119,136,153), #778899
    "lightsteelblue": (176,196,222), #b0c4de
    "lightyellow": (255,255,224), #ffffe0
    "lime": (0,255,0), #00ff00
    "limegreen": (50,205,50), #32cd32
    "linen": (250,240,230), #faf0e6
    "magenta": (255,0,255), #ff00ff
    "maroon": (128,0,0), #800000
    "mediumaquamarine": (102,205,170), #66cdaa
    "mediumblue": (0,0,205), #0000cd
    "mediumorchid": (186,85,211), #ba55d3
    "mediumpurple": (147,112,219), #9370db
    "mediumseagreen": (60,179,113), #3cb371
    "mediumslateblue": (123,104,238), #7b68ee
    "mediumspringgreen": (0,250,154), #00fa9a
    "mediumturquoise": (72,209,204), #48d1cc
    "mediumvioletred": (199,21,133), #c71585
    "midnightblue": (25,25,112), #191970
    "mintcream": (245,255,250), #f5fffa
    "mistyrose": (255,228,225), #ffe4e1
    "moccasin": (255,228,181), #ffe4b5
    "navajowhite": (255,222,173), #ffdead
    "navy": (0,0,128), #000080
    "oldlace": (253,245,230), #fdf5e6
    "olive": (128,128,0), #808000
    "olivedrab": (107,142,35), #6b8e23
    "orange": (255,165,0), #ffa500
    "orangered": (255,69,0), #ff4500
    "orchid": (218,112,214), #da70d6
    "palegoldenrod": (238,232,170), #eee8aa
    "palegreen": (152,251,152), #98fb98
    "paleturquoise": (175,238,238), #afeeee
    "palevioletred": (219,112,147), #db7093
    "papayawhip": (255,239,213), #ffefd5
    "peachpuff": (255,218,185), #ffdab9
    "peru": (205,133,63), #cd853f
    "pink": (255,192,203), #ffc0cb
    "plum": (221,160,221), #dda0dd
    "powderblue": (176,224,230), #b0e0e6
    "purple": (128,0,128), #800080
    "red": (255,0,0), #ff0000
    "rosybrown": (188,143,143), #bc8f8f
    "royalblue": (65,105,225), #4169e1
    "saddlebrown": (139,69,19), #8b4513
    "salmon": (250,128,114), #fa8072
    "sandybrown": (244,164,96), #f4a460
    "seagreen": (46,139,87), #2e8b57
    "seashell": (255,245,238), #fff5ee
    "sienna": (160,82,45), #a0522d
    "silver": (192,192,192), #c0c0c0
    "skyblue": (135,206,235), #87ceeb
    "slateblue": (106,90,205), #6a5acd
    "slategray": (112,128,144), #708090
    "slategrey": (112,128,144), #708090
    "snow": (255,250,250), #fffafa
    "springgreen": (0,255,127), #00ff7f
    "steelblue": (70,130,180), #4682b4
    "tan": (210,180,140), #d2b48c
    "teal": (0,128,128), #008080
    "thistle": (216,191,216), #d8bfd8
    "tomato": (255,99,71), #ff6347
    "turquoise": (64,224,208), #40e0d0
    "violet": (238,130,238), #ee82ee
    "wheat": (245,222,179), #f5deb3
    "white": (255,255,255), #ffffff
    "whitesmoke": (245,245,245), #f5f5f5
    "yellow": (255,255,0), #ffff00
    "yellowgreen": (154,205,50) #9acd32
}

class JSTurtle:
    curx = 0
    cury = 0
    heading = 0

    def home(self):
        turtle.goto(0, 0)
        turtle.setheading(0)
        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def move(self, distance):
        if distance < 0:
            turtle.backward(-distance)
        else:
            turtle.forward(distance)

        (self.curx, self.cury), self.heading = turtle.position(), turtle.heading()

    def turn(self, angle):
        if angle < 0:
            turtle.left(-angle)
        else:
            turtle.right(angle)

        self.heading = turtle.heading()

    def wait(self, interval):
        # argument time is 1/60 of seconds
        time.sleep(interval * 1.0/60.0)

    def setvar(self, varname, value):
        if varname == "led1":
            turtle.leftLED.value = value != 0
        elif varname == "led2":
            turtle.rightLED.value = value != 0
        elif varname == "ir1":
            turtle.leftDetector.value = value != 0
        elif varname == "ir2":
            turtle.rightDetector.value = value != 0
        elif varname == "emitter":
            turtle.emitter.value = value != 0
        else:
            pass

    def not_supported(self):
        turtle.tone(4500, 0.1)

    def not_implemented(self):
        turtle.tone(1000, 0.2)

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

        # Without moving the turtle, draws an arc centered on the
        # turtle, starting at the turtle's heading

        px, py = self.curx, self.cury
        heading = self.heading

        self.pendown(False)
        self.turn(angle)
        self.move(radius)
        self.pendown(True)
        turtle.circle(radius, angle)
        self.pendown(False)
        turtle.goto(px, py)
        turtle.setheading(heading)

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
        c = color.lower()
        if c[0] == "#" and len(c) == 7:
            r = int(c[1:3], 16)
            g = int(c[3:5], 16)
            b = int(c[5:7], 16)
            col = (r, g, b)
        elif c in _CSS_COLORS:
            col = _CSS_COLORS[c]
        else:
            self.not_supported() # unrecognized, leave color unchanged
            return

        # ask user for pen change
        turtle.rgbLED[0] = col

        # wait for button to be pushed
        br = 0.3
        while not turtle.isButtonPushed():
            turtle.rgbLED.brightness = br
            time.sleep(0.1)
            br -= 0.1
            if br <= 0:
                br = 0.3

        turtle.rgbLED.brightness = 0.2

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

    def setheading(self, angle):
        turtle.setheading(angle)

    def visible(self, visible):
        if not visible:
            # don't know how to make things invisible
            self.not_supported()

    def scrunch(self, sc):
        self.not_implemented()



