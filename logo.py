#!/bin/env python3
#
# CircuitPython interpreter for jslogo.
#
# Author: Sreepathi Pai
# Copyright (C) 2023 University of Rochester
#
# Licensed under the MIT License
#
# This is a reimplementation of logo.js in Python since it still uses
# the Logo interface. Error checking is minimal in this version since
# it assumes the code it will run has already been executed
# successfully.
#
# The original copyright for that code written in JavaScript is:
#
# Copyright (C) 2011 Joshua Bell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import re

NUMBER = re.compile("-?([0-9]*\\.?[0-9]+([eE][\\-+]?[0-9]+)?)")
UNARY_MINUS = '<UNARYMINUS>'

class StringMap:
    def __init__(self, case_fold):
        self._case_fold = case_fold
        self._map = {}

    def get(self, key):
        key = key if not self._case_fold else key.lower()
        return self._map.get(key, None)

    def set(self, key, value):
        key = key if not self._case_fold else key.lower()
        self._map[key] = value

    def has(self, key):
        key = key if not self._case_fold else key.lower()
        return key in self._map

    def delete(self, key):
        key = key if not self._case_fold else key.lower()
        del self._map[key]

    def keys(self):
        return self.keys()

    def empty(self):
        return len(self._map) == 0

    # forEach

class Logo:
    def __init__(self, turtle):
        self.turtle = turtle
        self.routines = StringMap(True)
        self.stack = []
        self._repcount = 0
        self.define_motion()
        self.define_control()

    def run(self, code):
        return self.evaluateExpression(code)

    def define(self, names, code, nargs, props = None):
        if props is None: props = {}

        props['args'] = nargs

        for n in names:
            self.routines.set(n, {'code': code, 'props': props})

    # motion
    def forward(self, a):
        return self.turtle.move(self.aexpr(a))

    def back(self, a):
        return self.turtle.move(-self.aexpr(a))

    def left(self, a):
        return self.turtle.turn(-self.aexpr(a))

    def right(self, a):
        return self.turtle.turn(self.aexpr(a))

    # no support for arrows

    def setpos(self, l):
        l = self.lexpr(l)
        assert len(l) == 2, "Need list of length 2 for setpos"
        self.turtle.position([self.aexpr(l[0]), self.aexpr(l[1])])

    def setxy(self, x, y):
        self.turtle.position([self.aexpr(x), self.aexpr(y)])

    def setx(self, x):
        self.turtle.position([self.aexpr(x), self.turtle.cury])

    def sety(self, y):
        self.turtle.position([self.turtle.curx, self.aexpr(y)])

    def setheading(self, heading):
        self.turtle.setheading(self.aexpr(heading))

    def home(self):
        # TODO
        return self.turtle.home()

    def arc(self, angle, radius):
        # TODO: what does this return?
        return self.turtle.arc([self.aexpr(angle), self.aexpr(radius)])

    # motion queries

    def pos(self):
        return [self.turtle.curx, self.turtle.cury]

    def xcor(self):
        return self.turtle.curx

    def ycor(self):
        return self.turtle.cury

    def heading(self):
        return self.turtle.heading

    def towards(self, l):
        l = self.lexpr(l)

        assert len(l) == 2, "towards expects list of length 2"

        return self.turtle.towards(self.aexpr(l[0]), self.aexpr(l[1]))

    # scrunch

    # clean, wrap, window, fence, fill, filled, label, setlabelheight, setlabelfont
    # setscrunch
    # shownp, turtlemode, labelsize, labelfont

    def clearscreen(self):
        self.turtle.clearscreen()

    def penup(self):
        self.turtle.pendown(False)

    def pendown(self):
        self.turtle.pendown(True)

    # penpaint, penerase, penreverse

    # TODO: setpencolor, setpc, setcolor

    # setpalette, setpensize, setwidth, setpw
    # setbackground, setbg, setscreencolor, setsc

    def pendownp(self):
        return 1 if self.turtle.pendownp() else 0

    def buttonp(self):
        return 1 if self.turtle.buttonp() else 0

    def define_motion(self):
        self.define(['forward', 'fd'], self.forward, 1)
        self.define(['back', 'bk'], self.back, 1)
        self.define(['left', 'lt'], self.left, 1)
        self.define(['right', 'rt'], self.right, 1)

        self.define(['setpos'], self.setpos, 1)
        self.define(['setxy'], self.setxy, 1)
        self.define(['setx'], self.setx, 1)
        self.define(['sety'], self.sety, 1)
        self.define(['setheading', 'seth'], self.setheading, 1)

        self.define(['home'], self.home, 0)
        self.define(['arc'], self.arc, 2)
        self.define(['pos'], self.pos, 0)
        self.define(['xcor'], self.xcor, 0)
        self.define(['ycor'], self.ycor, 0)
        self.define(['heading'], self.heading, 0)
        self.define(['towards'], self.towards, 1)

        self.define(['clearscreen'], self.clearscreen, 0)
        self.define(['pendown', 'pd'], self.pendown, 0)
        self.define(['penup', 'pu'], self.penup, 0)

        self.define(['pendownp', 'pendown?'], self.pendownp, 0)
        self.define(['buttonp', 'button?'], self.buttonp, 0)

    # control
    def repeat(self, count, statements):
        count = self.aexpr(count)
        statements = self.lexpr(statements)
        old_repcount = self._repcount
        i = 1

        while not (i > count):
            self.execute(statements)
            i += 1
            self._repcount = i

        self._repcount = old_repcount

    def repcount(self):
        return self._repcount

    def forever(self, statements):
        statements = self.lexpr(statements)
        old_repcount = self._repcount
        i = 1

        while True:
            self.execute(statements)
            i += 1
            self._repcount = i

        self._repcount = old_repcount

    def define_control(self):
        # TODO: run, runresult
        self.define(['repeat'], self.repeat, 2)
        self.define(['forever'], self.forever, 1)
        self.define(['repcount', '#'], self.repcount, 0)

    # err

    # to_arity?

    # PRNG?

    # StringMap?

    # LogoArray?

    # Stream?

    # routines, scopes, plists?

    # Type

    def Type(self, atom):
        assert atom is not None, "Type, Atom should not be none"

        if isinstance(atom, str) or isinstance(atom, (float, int)):
            return 'word'
        elif isinstance(atom, list): # TODO: LogoArray
            return 'array'
        elif not atom:
            assert False, "Unexpected value for atom"
        else:
            assert False, "Unknown type"

    # all parsing routines omitted
    # reparse?
    # maybegetvar
    # getvar
    # lvalue
    # setvar
    # local
    # set local

    def execute(self, statements, options = None):
        statements = list(statements) # shallow copy [.slice in original]

        while len(statements):
            result = self.evaluateExpression(statements)
            # TODO: return result?
            lastResult = result

        return lastResult

    def isNumber(self, atom):
        m = NUMBER.match(str(atom))
        if NUMBER.match(str(atom)) is not None:
            return True

        return False

    def peek(self, l, options):
        if len(l):
            n = l[0]
            return n in options

        return False

    def evaluateExpression(self, l):
        return self.expression(l)

    def expression(self, l):
        return self.relationalExpression(l)

    def relationalExpression(self, l):
        lhs = self.additiveExpression(l)

        while self.peek(l, ['=', '<', '>', '<=', '>=', '<>']):
            op = l.pop(0)
            rhs = self.additiveExpression(l)

            if op == '<':
                lhs = 1 if self.aexpr(lhs) < self.aexpr(rhs) else 0
            elif op == '>':
                lhs = 1 if self.aexpr(lhs) > self.aexpr(rhs) else 0
            elif op == '=':
                lhs = 1 if self.equal(lhs, rhs) else 0
            elif op == '<=':
                lhs = 1 if  self.aexpr(lhs) <= self.aexpr(rhs) else 0
            elif op == '>=':
                lhs = 1 if self.aexpr(lhs) >= self.aexpr(rhs) else 0
            elif op == '<>':
                lhs = 1 if not self.equal(lhs, rhs) else 0
            else:
                assert False, "Internal error in relationalExpression"

        return lhs

    def additiveExpression(self, l):
        lhs = self.multiplicativeExpression(l)

        while self.peek(l, ['+', '-']):
            op = l.pop(0)
            rhs = self.multiplicativeExpression(l)

            if op == '+':
                lhs = self.aexpr(lhs) + self.aexpr(rhs)
            elif op == '-':
                lhs = self.aexpr(lhs) - self.aexpr(rhs)
            else:
                assert False, "Internal error in additiveExpression"

        return lhs

    def multiplicativeExpression(self, l):
        lhs = self.powerExpression(l)

        while self.peek(l, ['*', '/', '%']):
            op = l.pop(0)
            rhs = self.powerExpression(l)

            if op == '*':
                lhs = self.aexpr(lhs) * self.aexpr(rhs)
            elif op == '/':
                n = self.aexpr(lhs)
                d = self.aexpr(rhs)
                lhs = n / d
            elif op == '%':
                n = self.aexpr(lhs)
                d = self.aexpr(rhs)
                lhs = n % d
            else:
                assert False, "Internal error in multiplicativeExpression"

        return lhs

    def powerExpression(self, l):
        lhs = self.unaryExpression(l)

        while self.peek(l, ['^']):
            op = l.pop(0)
            rhs = self.unaryExpression(l)
            lhs = math.pow(aexpr(lhs), aexpr(rhs))

        return lhs

    def unaryExpression(self, l):
        if self.peek(l, [UNARY_MINUS]):
            op = l.pop(0)
            rhs = self.unaryExpression(l)
            return -self.aexpr(rhs)
        else:
            return self.finalExpression(l)

    def finalExpression(self, l):
        assert len(l), "Unexpected end of instructions"

        atom = l.pop(0)
        ty = self.Type(atom)

        if ty == 'array' or ty == 'list':
            return atom
        elif ty == 'word':
            if self.isNumber(atom):
                return float(atom)

            if atom[0] == '"' or atom[0] == "'":
                return atom[1:]

            if atom[0] == ':':
                return self.getvar(atom[1:])

            if atom[0] == '(':
                # TODO: check for list-style procedure input calling syntax

                result = self.expression(l)

                assert len(l), "Expecting ')', but list is empty"
                assert self.peek(l, [')']), "Expecting ')', but got something else"
                l.pop(0)
                return result

            if atom == ')':
                assert False, "Unexpected )"

            return self.dispatch(atom, l, True)
        else:
            assert False, "Internal error in finalExpression"

    def dispatch(self, name, tokenlist, natural):
        name = name.upper()
        proc = self.routines.get(name)
        if proc is None:
            assert False, "ERROR: {} undefined".format(name)

        if proc['props'].get('special', False):
            raise NotImplementedError

        if natural:
            args = []
            for i in range(proc['props'].get('args')):
                args.append(self.expression(tokenlist))
        else:
            raise NotImplementedError

        if proc['props'].get('noeval', False):
            raise NotImplementedError

        self.stack.append(name)
        rv = proc['code'](*args)
        self.stack.pop()
        return rv

    def aexpr(self, atom):
        if atom is not None and self.Type(atom) == 'word':
            if self.isNumber(atom):
                return float(atom)

        assert False, "Expecting number"

    def lexpr(self, atom):
        assert atom is not None
        if self.Type(atom) == 'word':
            raise NotImplementedError
        else:
            return self.copy(atom)

    def copy(self, value):
        if self.Type(value) == 'list':
            return list(value)
        else:
            return value

    def equal(self, a, b):
        at = self.Type(a)
        bt = self.Type(b)

        if at != bt: return False

        if at == 'word':
            if isinstance(a, (int, float)) or isinstance(b, (int, float)):
                return a == b
            else:
                return str(a) == str(b)
        elif at == 'list':
            if a.length != b.length:
                return False

            for i in range(len(a)):
                if not self.equal(a[i], b[i]):
                    return False

            return True
        elif at == 'array':
            raise NotImplementedError("equal for array types not implemented")

        assert False, "Unexpected flow in equal" # or return None?

