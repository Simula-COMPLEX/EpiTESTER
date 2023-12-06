# -*- coding: utf-8 -*-
# file  :  selectionoperator.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from abc import ABC, abstractmethod
from ..epigeneticpopulation import EpigeneticPopulation


class SelectionOperator(ABC):
    """Selection Operator."""

    @abstractmethod
    def select(self, pop):
        """
        Selects a new set of EpigeneticIndividuals.

        :param EpigeneticPopulation pop: the EpigeneticPopulation.
        """
        pass