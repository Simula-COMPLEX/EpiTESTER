# -*- coding: utf-8 -*-
# file  :  nucleosomegenerator.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from ..epigeneticpopulation import EpigeneticPopulation


class NucleosomeGenerator():
    """Nucleosome Generator."""

    def __init__(self, p_n, radius):
        """
        Constructor.

        :param float p_n: the nucleosome probability.
        :param int radius: the nucleosome radius.
        """
        self.__p_n = p_n
        self.__radius = radius

    def generate(self, pop):
        """Generate and update the nucleosomes in all the EpigeneticCells in all the EpigeneticIndividuals in the
        EpigeneticPopulation.

        :param EpigeneticPopulation pop: the EpigeneticPopulation.
        """
        for i in range(pop.size):
            for cell in pop.get(i).cells:
                cell.generate_nucleosomes(self.__p_n, self.__radius)
