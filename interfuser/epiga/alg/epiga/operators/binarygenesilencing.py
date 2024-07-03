# -*- coding: utf-8 -*-
# file  :  binarygenesilencing.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from .epigeneticoperator import EpigeneticOperator


class BinaryGeneSilencing(EpigeneticOperator):
    """Binary Gene Silencing Operator."""

    def __init__(self, p_e):
        """
        Constructor.

        :param float p_e: the epigenetic probability
        """
        super().__init__(p_e)

    def methylate(self, pop):
        env = pop.problem.environment
        for i in range(pop.size):
            for cell in pop.get(i).cells:
                for j in range(len(cell.solution)):
                    if cell.nucleosomes[j] and random.random() < self._p_e:
                        cell.solution[j] = random.random() < env[j]
