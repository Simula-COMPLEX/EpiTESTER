#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 05.09.2023 11:52
# @Author  : 
# @File    : equation_solver.py
# @Software: PyCharm
import unittest
from sympy.solvers import solve
from sympy import Symbol


class TestEquSolver(unittest.TestCase):
    def test_solver(self, ego, npc):
        TTC = Symbol('TTC')
        result = solve(((ego.get_location().x + ego.get_velocity().x * TTC +
                         1 / 2 * ego.get_acceleration().x * TTC ** 2) -
                        (npc.get_location().x + npc.get_velocity().x * TTC +
                         1 / 2 * npc.get_acceleration().x * TTC ** 2) ** 2) -

                       ((ego.get_location().y + ego.get_velocity().y * TTC +
                         1 / 2 * ego.get_acceleration().y * TTC ** 2) -
                        (npc.get_location().y + npc.get_velocity().y * TTC +
                         1 / 2 * npc.get_acceleration().y * TTC ** 2) ** 2)
                       )
        print(result)
