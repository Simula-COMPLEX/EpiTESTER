# -*- coding: utf-8 -*-
# file  :  epigeneticindividual.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from .epigeneticcell import EpigeneticCell
from .problems.problem import Problem


class EpigeneticIndividual:
    """Epigenetic Individual."""

    def __init__(self, problem, n_cells, cells=None):
        """
        Constructor.

        :param Problem problem: the problem.
        :param int n_cells: the number of cells
        :param list[EpigeneticCell] cells: an optional list of EpigeneticCells of size n_cells.
        """
        self.__problem = problem
        if cells is None:
            self.__cells = [EpigeneticCell(self.__problem) for _ in range(n_cells)]
        else:
            self.__cells = cells

    def __str__(self):
        string = ""
        for n, cell in enumerate(self.__cells, start=1):
            string += "Cell {}:\n".format(n) + str(cell) + "\n"
        return string

    def duplicate(self):
        """
        Duplicates the EpigeneticIndividual.

        :return: a copy of the EpigeneticIndividual.
        :rtype: EpigeneticIndividual
        """
        temp_list = list()
        for c in self.__cells:
            temp_list.append(EpigeneticCell(self.__problem, c.nucleosomes, c.solution, c.fitness))
        return EpigeneticIndividual(self.__problem, len(temp_list), temp_list)

    def replicate(self):
        """
        Duplicates the EpigeneticIndividual and set all its cells as a copy of the best EpigeneticCell.

        :return: a copy of the EpigeneticIndividual.
        :rtype: EpigeneticIndividual
        """
        temp_list = list()
        c = self.get_best_cell()
        for i in range(len(self.__cells)):
            temp_list.append(c.duplicate())
        return EpigeneticIndividual(self.__problem, len(temp_list), temp_list)

    def evaluate(self):
        """Evaluates the EpigeneticIndividual by evaluating of the EpigeneticCells in it."""
        for cell in self.__cells:
            cell.evaluate()

    def get_best_cell(self):
        """
        Returns the best EpigeneticCell in the EpigeneticIndividual.

        :return: the best EpigeneticCell in the EpigeneticIndividual.
        :rtype: EpigeneticCell
        """
        best_c = None
        for c in self.__cells:
            if c.is_better(best_c):
                best_c = c
        return best_c

    def get_best_fitness(self):
        """
        Returns the fitness of the best EpigeneticCell in the EpigeneticIndividual.

        :return: the fitness of the best EpigeneticCell in the EpigeneticIndividual.
        :rtype: float
        """
        return self.get_best_cell().fitness

    def is_better(self, individual):
        """
        Returns **True** if the EpigeneticIndividual is better than ``individual``.

        :param EpigeneticIndividual individual: the individual.
        :return: True if the EpigeneticIndividual is better than individual.
        :rtype: bool
        """
        return self.get_best_cell().is_better(individual.get_best_cell())

    @property
    def cells(self):
        """Returns the EpigeneticCells in the EpigeneticIndividual.

        :return: the EpigeneticCells in the EpigeneticIndividual.
        :rtype: list[EpigeneticCell]
        """
        return self.__cells

    @property
    def problem(self):
        """
        Returns the Problem.

        :return: the problem.
        :rtype: Problem
        """
        return self.__problem
