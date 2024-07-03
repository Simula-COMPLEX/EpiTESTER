# -*- coding: utf-8 -*-
# file  :  floatproblem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from abc import ABC
from .numericproblem import NumericProblem


class FloatProblem(NumericProblem, ABC):
    """
    Float problem.
    Represents problems represented as Float numbers.
    """

    def generate_solution(self):
        sol = list()
        for i in range(self.size):
            low, upp = self.limits(i)
            sol.append(random.random() * (upp - low) + low)
        return sol

    def delta(self, position):
        low, upp = self.limits(position)
        m = random.randint(1, 10)
        return self.k(position) * (upp - low) / m

    def _format(self, position):
        return "{:9.3f}"
