# -*- coding: utf-8 -*-
# file  :  binaryproblem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from abc import ABC
from .problem import Problem


class BinaryProblem(Problem, ABC):
    """
    Binary problem.
    Represents problems represented as Binary numbers as KP, MKP, OneMax, etc.
    """

    def generate_solution(self):
        return [random.random() < 0.5 for _ in range(self.size)]

    def limits(self, position):
        return False, True

    def format_solution(self, solution):
        str_solution = ""
        for s in solution:
            str_solution += "1 " if s else "0 "
        return str_solution

    def delta(self, position):
        pass

    def repair(self, solution):
        return solution
