# -*- coding: utf-8 -*-
# file  :  replacementoperator.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from abc import ABC, abstractmethod

class ReplacementOperator(ABC):
    """Replacement Operator."""

    @abstractmethod
    def replace(self, pop, temp):
        """
        Returns a new EpigeneticPopulation after replacing the EpigeneticIndividuals in the EpigeneticPopulation
        ``pop`` using the EpigeneticIndividuals in ``temp``.

        :param EpigeneticPopulation pop: the initial EpigeneticPopulation.
        :param EpigeneticPopulation temp: the temporal EpigeneticPopulation.
        :return: a new EpigeneticPopulation after replacement.
        :rtype: EpigeneticPopulation
        """
        pass