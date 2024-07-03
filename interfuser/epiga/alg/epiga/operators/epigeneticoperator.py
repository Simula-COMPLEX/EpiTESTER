# -*- coding: utf-8 -*-
# file  :  epigeneticoperator.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from abc import ABC, abstractmethod
from ..epigeneticpopulation import EpigeneticPopulation


class EpigeneticOperator(ABC):
    """Epigenetic Operator."""

    def __init__(self, p_e):
        """
        Constructor.

        :param float p_e: the epigenetic probability
        """
        self._p_e = p_e

    @abstractmethod
    def methylate(self, pop):
        """
        DNA Methylation of all the EpigeneticCells of all the EpigeneticIndividuals in the EpigeneticPopulation.

        :param EpigeneticPopulation pop: the EpigeneticPopulation.
        """
        pass
