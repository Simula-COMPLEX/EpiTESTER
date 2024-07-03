# -*- coding: utf-8 -*-
# file  :  epigeneticcell.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import copy
import random
from .problems.problem import Problem


class EpigeneticCell:
    """Epigenetic Cell."""

    def __init__(self, problem, nucleosomes=None, solution=None, fitness=None):
        """
        Constructor.

        :param Problem problem: the problem.
        :param list[bool] nucleosomes: the nucleosome vector.
        :param list[Any] solution: the solution vector.
        :param float fitness: the fitness value.
        """
        self.__problem = problem
        if nucleosomes is None:
            self.__nucleosomes = [False for _ in range(self.__problem.size)]
        else:
            self.__nucleosomes = copy.deepcopy(nucleosomes)
        if solution is None:
            self.__solution = self.__problem.generate_solution()
        else:
            self.__solution = copy.deepcopy(solution)
        if fitness is None:
            self.evaluate()
        else:
            self.__fitness = fitness

    def __str__(self):
        str_nucleosomes = ""
        for n in self.__nucleosomes:
            str_nucleosomes += "1 " if n else "0 "
        return "Solution: " + self.__problem.format_solution(self.__solution) + "\nFitness: {:.3f}".format(
            self.__fitness) + "\nNucleosomes: " + str_nucleosomes + "\n"

    def duplicate(self):
        """
        Duplicates the EpigeneticCell.

        :return: a copy of the EpigeneticCell.
        :rtype: EpigeneticCell
        """
        return EpigeneticCell(self.__problem, self.__nucleosomes, self.__solution, self.__fitness)

    def evaluate(self):
        """
        Repairs and Evaluates the EpigeneticCell and update its fitness.
        """
        self.__solution = self.__problem.repair(self.__solution)
        self.__fitness = self.__problem.compute_fitness(self.__solution)

    def is_better(self, cell):
        """
        Returns **True** if the EpigeneticCell is better than ``cell``.

        :param EpigeneticCell cell: the EpigeneticCell.
        :return: True if the EpigeneticCell is better than cell.
        :rtype: EpigeneticCell
        """
        return cell is None or self.__problem.compare(self.__fitness, cell.fitness)

    def generate_nucleosomes(self, p_n, radius):
        """
        Generates and updates the nucleosomes in the cell.

        :param float p_n: the nucleosome probability.
        :param int radius: the nucleosome radius.
        :rtype: None
        """
        size = self.__problem.size
        self.__nucleosomes = [False for _ in range(size)]
        i = 0
        while i < size:
            if random.random() < p_n:
                ini = i - radius
                end = i + radius
                for j in range(ini, end + 1):
                    if 0 <= j < size:
                        self.__nucleosomes[j] = True
                i = end
            i += 1

    @property
    def fitness(self):
        """
        Returns the fitness value.

        :return: the fitness value.
        :rtype: float
        """
        return self.__fitness

    @property
    def solution(self):
        """
        Returns the solution vector.

        :return: the solution vector.
        :rtype: list[Any]
        """
        return self.__solution

    @property
    def nucleosomes(self):
        """
        Returns the nucleosome vector.

        :return: the nucleosome vector.
        :rtype: list[bool]
        """
        return self.__nucleosomes

    @property
    def problem(self):
        """
        Returns the Problem.

        :return: the problem.
        :rtype: Problem
        """
        return self.__problem
