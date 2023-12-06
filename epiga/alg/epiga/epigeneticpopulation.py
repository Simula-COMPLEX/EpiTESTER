# -*- coding: utf-8 -*-
# file  :  epigeneticpopulation.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
from .epigeneticexception import EpigeneticException
from .epigeneticindividual import EpigeneticIndividual
from .problems.problem import Problem


class EpigeneticPopulation:
    """Epigenetic Population."""

    def __init__(self, problem):
        """
        Constructor.

        :param Problem problem: the problem.
        """
        self.__problem = problem
        self.__pop = []

    def __str__(self):
        string = ""
        for n, ind in enumerate(self.__pop, start=1):
            string += "Individual {}:\n".format(n) + str(ind)
        return string

    def generate(self, n_individuals, n_cells):
        """
        Fills the population.

        :param int n_individuals: the number of EpigeneticIndividuals.
        :param int n_cells: the number of EpigeneticCells.
        :rtype: None
        :raise EpigeneticException: if params are not greater than zero.
        """
        if n_individuals == 0:
            raise EpigeneticException("Number of individuals cannot be 0")
        if n_cells == 0:
            raise EpigeneticException("Number of cells cannot be 0")
        self.__pop = [EpigeneticIndividual(self.__problem, n_cells) for _ in range(n_individuals)]

    def evaluate(self):
        """Evaluates the EpigeneticPopulation."""
        for ind in self.__pop:
            ind.evaluate()

    def get(self, pos):
        """
        Returns the EpigeneticIndividual in the position.

        :param int pos: the position [0 -- size-1]
        :return: the EpigeneticIndividual in the position.
        :rtype: EpigeneticIndividual
        """
        return self.__pop[pos]

    def add(self, individual):
        """
        Adds the EpigeneticIndividual to the position and returns the EpigeneticPopulation.

        :param EpigeneticIndividual individual: the individual.
        :return: the resulting EpigeneticPopulation.
        :rtype: EpigeneticPopulation
        """
        return self.__pop.append(individual)

    def metrics(self):
        """
        Returns the mean and best fitness of the EpigeneticPopulation.

        :return: the mean and best fitness of the EpigeneticPopulation.
        :rtype: (float,float)
        """
        best_i = self.__pop[0]
        sum_f = 0
        best_f = None
        for ind in self.__pop:
            f = ind.get_best_fitness()
            sum_f += f
            if ind.is_better(best_i):
                best_i = ind
                best_f = f
        return sum_f / self.size, best_f

    def best_individual(self):
        """
        Returns the best EpigeneticIndividual in the EpigeneticPopulation.

        :return: the best EpigeneticIndividual in the EpigeneticPopulation.
        :rtype: EpigeneticIndividual
        """
        best_i = self.__pop[0]
        for ind in self.__pop:
            if ind.is_better(best_i):
                best_i = ind
        return best_i

    @property
    def problem(self):
        """
        Returns the Problem.

        :return: the problem.
        :rtype: Problem
        """
        return self.__problem

    @property
    def size(self):
        """
        Returns the number of EpigeneticIndividuals in the EpigeneticPopulation.

        :return: the number of EpigeneticIndividuals in the EpigeneticPopulation.
        :rtype: int
        """
        return len(self.__pop)

    def check(self):
        """Checks the EpigeneticPopulation using **assert**."""
        for i1 in range(len(self.__pop)):
            for i2 in range(i1 + 1, len(self.__pop)):
                assert (self.__pop[i1] is not self.__pop[i2])
                for c1 in range(len(self.__pop[i1].cells)):
                    for c2 in range(c1 + 1, len(self.__pop[i1].cells)):
                        assert (self.__pop[i1].cells[c1] is not self.__pop[i2].cells[c2])
