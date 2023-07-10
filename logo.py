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

class Logo:
    def __init__(self, turtle):
        self.turtle = turtle

    def run(self, code):
        return self.evaluateExpression(code)

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

            self.dispatch(atom, l, true)
        else:
            assert False, "Internal error in finalExpression"

    def dispatch(self, name, tokenlist, natural):
        raise NotImplementedError

    def aexpr(self, atom):
        if atom is not None and self.Type(atom) == 'word':
            if self.isNumber(atom):
                return float(atom)

        assert False, "Expecting number"

    # TODO: copy, equal
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

