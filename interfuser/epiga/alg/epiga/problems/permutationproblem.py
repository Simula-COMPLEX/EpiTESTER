# -*- coding: utf-8 -*-
# file  :  permutationproblem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from abc import ABC

from .problem import Problem


class PermutationProblem(Problem, ABC):
    """
    Permutation problem.
    Represents problems involving permutations like TSP, Graph Colouring Problem, etc.
    """

    def __init__(self, name, elements, environment, maxmin):
        """
        Problem Constructor.

        :param str name: the problem name.
        :param list elements: the elements used in the problem solution.
        :param list[float] environment: a probability list corresponding to the epigenetic environment.
        :param int maxmin: maximization/minimization problem (Problem.MAXIMIZATION or Problem.MINIMIZATION).
        """
        super().__init__(name, len(elements), environment, maxmin)
        self._elements = elements

    def __str__(self):
        str_pr = super().__str__() + "\nElements: "
        for el in self._elements:
            str_pr += "{} ".format(el)
        return str_pr

    def limits(self, position):
        pass

    def generate_solution(self):
        temp: list = self._elements[1:]
        result = list()
        result.append(self._elements[0])
        while len(temp) > 1:
            result.append(temp.pop(random.randint(0, len(temp) - 1)))
        result.append(temp.pop())
        return result

    def format_solution(self, solution):
        str_solution = ""
        for i in range(len(solution)):
            str_solution += "{} ".format(solution[i])
        return str_solution

    def delta(self, position):
        pass

    def repair(self, solution):
        missing = self._elements[:]
        repaired = list()
        for i, el in enumerate(solution):
            if el in missing:
                missing.remove(el)
            if el not in solution[i + 1:]:
                repaired.append(el)
        repaired.extend(missing)
        return repaired
