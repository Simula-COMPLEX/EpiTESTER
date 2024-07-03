# -*- coding: utf-8 -*-
# file  :  integerproblem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from abc import ABC
from .numericproblem import NumericProblem


class IntegerProblem(NumericProblem, ABC):
    """
    Integer problem.
    Represents problems represented as Integer numbers.
    """

    def generate_solution(self):
        sol = list()
        for i in range(self.size):
            low, upp = self.limits(i)
            sol.append(random.randint(low, upp))
        return sol

    def delta(self, position):
        low, upp = self.limits(position)
        m = random.randint(1, 10)
        return int(round(self.k(position) * (upp - low) / m))

    def _format(self, position):
        return "{:6d}"
