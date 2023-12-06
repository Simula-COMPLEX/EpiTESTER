# -*- coding: utf-8 -*-
# file  :  elitistreplacement.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
from .replacementoperator import ReplacementOperator
from ..epigeneticpopulation import EpigeneticPopulation
from ..epigeneticpopulation import EpigeneticIndividual


class ElitistReplacement(ReplacementOperator):
    """Elitist Replacement Operator."""

    def __init__(self, duplicates=True):
        """
        Constructor.

        :param bool duplicates: True (default) to allow repeated EpigeneticIndividuals in the resulting EpigeneticPopulation.
        """
        self.__duplicates = duplicates

    def replace(self, pop, temp):

        l1 = list()
        for i in range(pop.size):
            l1.append(pop.get(i))
        for i in range(temp.size):
            l1.append(temp.get(i))

        l2 = sorted(l1, reverse=pop.problem.maximization, key=lambda x: x.get_best_fitness())

        result = EpigeneticPopulation(pop.problem)
        l = list()
        i = 0
        while i < pop.size and result.size < pop.size:
            v = hash(tuple(l2[i].get_best_cell().solution))
            if self.__duplicates or v not in l:
                result.add(l2[i].replicate())
                l.append(v)
            i += 1
        for i in range(result.size, pop.size):
            result.add(EpigeneticIndividual(pop.problem, len(pop.get(0).cells)))

        return result
