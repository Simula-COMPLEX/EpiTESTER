# -*- coding: utf-8 -*-
# file  :  binarytournamentselection.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random

from .selectionoperator import SelectionOperator
from ..epigeneticpopulation import EpigeneticPopulation


class BinaryTournamentSelection(SelectionOperator):
    """Binary Tournament Selection Operator."""

    def select(self, pop):
        temp = EpigeneticPopulation(pop.problem)

        for n in range(pop.size):
            i1 = pop.get(random.randint(0, pop.size - 1))
            i2 = pop.get(random.randint(0, pop.size - 1))
            if i1.is_better(i2):
                temp.add(i1.duplicate())
            else:
                temp.add(i2.duplicate())
        return temp
