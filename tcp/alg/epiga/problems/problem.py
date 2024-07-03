# -*- coding: utf-8 -*-
# file  :  problem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from abc import ABC, abstractmethod

from ..epigeneticexception import EpigeneticException


class Problem(ABC):
    """Problem."""

    MAXIMIZATION = 0
    MINIMIZATION = 1

    def __init__(self, name, size, environment, maxmin):
        """
        Problem Constructor.

        :param str name: the problem name.
        :param int size: the size of the problem solution.
        :param list[float] environment: a probability list corresponding to the epigenetic environment.
        :param int maxmin: maximization/minimization problem (Problem.MAXIMIZATION or Problem.MINIMIZATION).
        :raise EpigeneticException: if maxmin is not Problem.MAXIMIZATION or Problem.MINIMIZATION.
        """
        self.__name = name
        self.__evaluations = 0
        self.__size = size
        self.__environment = environment
        self.__maxmin = maxmin
        if self.__maxmin != self.MAXIMIZATION and self.__maxmin != self.MINIMIZATION:
            raise EpigeneticException("Maxmin have to be Problem.MAXIMIZATION or Problem.MINIMIZATION")

    def __str__(self):
        str_pr = "Name: {}\nSize: {}\nOperation: ".format(self.__name, self.__size)
        str_pr += "MAXIMIZATION" if self.__maxmin == self.MAXIMIZATION else "MINIMIZATION"
        str_pr += "\nEvaluations: {}".format(self.__evaluations)
        return str_pr

    def compute_fitness(self, solution):
        """
        Computes the fitness of the solution.

        :param list[Any] solution: the representation of the solution.
        :return: the fitness value.
        :rtype: float
        :raise EpigeneticException: if the solution length is wrong.
        """
        if len(solution) != self.size:
            raise EpigeneticException(
                "Wrong solution length {} when calculating fitness. It should be {}".format(len(solution), self.size))
        self.__evaluations += 1
        return self._get_fitness(solution)

    @abstractmethod
    def repair(self, solution):
        """
        Repairs the solution before evaluation if needed.

        :param list[Any] solution: the representation of the solution.
        :return: the repaired solution.
        :rtype: list[Any]
        """
        pass

    @abstractmethod
    def limits(self, position):
        """
        Returns the limits (min, max) of the variable in ``position``.

        :param int position: the position of the variable in the solution vector.
        :return: the limits.
        :rtype: (Any,Any)
        """
        pass

    @abstractmethod
    def generate_solution(self):
        """
        Generates a new solution.

        :return: a new solution.
        :rtype: list[Any]
        """
        pass

    def compare(self, f1, f2):
        """
        Returns **True** if *f1* is better than *f2*.

        :param float f1: the first fitness value.
        :param float f2: the second fitness value.
        :return: True if f1 is better than f2.
        :rtype: bool
        """
        if self.__maxmin == self.MAXIMIZATION:
            return f1 >= f2
        elif self.__maxmin == self.MINIMIZATION:
            return f1 <= f2

    @abstractmethod
    def _get_fitness(self, solution):
        """
        Calculates the fitness of the solution.

        :param list[Any] solution: the representation of the solution.
        :return: the fitness of the solution.
        :rtype: float
        """
        pass

    @abstractmethod
    def format_solution(self, solution):
        """
        Formats the solution vector.

        :param list[Any] solution: the representation of the solution.
        :return: the formatted solution vector.
        :rtype: str
        """
        pass

    @abstractmethod
    def delta(self, position):
        """
        Returns the *delta* increment when modifying the solution vector.

        :param int position: the position of the variable in the solution vector.
        :return: the delta increment.
        :rtype: Any
        """
        pass

    @property
    def minimization(self):
        """
        Returns **True** if it is a minimization problem.

        :return: True if it is a minimization problem.
        :rtype: bool
        """
        return self.__maxmin == self.MINIMIZATION

    @property
    def maximization(self):
        """
        Returns **True** if it is a maximization problem.

        :return: True if it is a maximization problem.
        :rtype: bool
        """
        return self.__maxmin == self.MAXIMIZATION

    @property
    def evaluations(self):
        """
        Returns the number of evaluations.

        :return: the number of evaluations.
        :rtype: int
        """
        return self.__evaluations

    @property
    def size(self):
        """
        Returns the problem size.

        :return: the problem size.
        :rtype: int
        """
        return self.__size

    @property
    def environment(self):
        """
        Returns the epigenetic environment.

        :return: the epigenetic environment.
        :rtype: list[bool]
        """
        return self.__environment
