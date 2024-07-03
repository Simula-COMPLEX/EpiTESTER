# -*- coding: utf-8 -*-
# file  :  numericproblem.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from abc import ABC, abstractmethod

from ..epigeneticexception import EpigeneticException
from .problem import Problem


class NumericProblem(Problem, ABC):
    """
    Represents Numeric problems.
    Its derived classes :class:`.IntegerProblem` and :class:`.FloatProblem` implements their respective types.
    """

    def __init__(self, name, size, minv, maxv, environment, maxmin):
        """
        Constructor.

        :param str name: the problem name.
        :param int size: the number of values in the solution vector.
        :param list[Any] minv: the lower limit of the variables.
        :param list[Any] maxv: the upper limit of the variables.
        :param list[float] environment: a probability list corresponding to the epigenetic environment.
        :param int maxmin: maximization/minimization problem (Problem.MAXIMIZATION or Problem.MINIMIZATION).
        :raise EpigeneticException: if the length of minv or maxv are different from the problem size.
        """
        super().__init__(name, size, environment, maxmin)
        if len(minv) != self.size:
            raise EpigeneticException("Wrong minv length {}. It sould be {}".format(len(minv), self.size))
        if len(maxv) != self.size:
            raise EpigeneticException("Wrong maxv length {}. It sould be {}".format(len(maxv), self.size))
        self.__minv = minv
        self.__maxv = maxv

    def __str__(self):
        str_pr = super().__str__() + "\nLower bound: "
        for i in range(len(self.__minv)):
            str_pr += self._format(i).format(self.__minv[i]) + " "
        str_pr += "\nUpper bound: "
        for i in range(len(self.__maxv)):
            str_pr += self._format(i).format(self.__maxv[i]) + " "
        return str_pr

    def format_solution(self, solution):
        str_solution = ""
        for i in range(len(solution)):
            str_solution += self._format(i).format(solution[i]) + " "
        return str_solution

    def limits(self, position):
        return self.__minv[position], self.__maxv[position]

    def k(self, position):
        """
        Attenuation coefficient of the variable in ``position`` usually depending on the maximum number of evaluations.
        k = 1 corresponds to no attenuation.

        :param int position: the position of the variable in the solution vector.
        :return: the attenuation coefficient.
        :rtype: float
        """
        return 1.0  # No attenuation by default. Override me!

    @abstractmethod
    def _format(self, position):
        """
        Numeric format pattern for the ``position``.

        :param int position: the position of the variable in the solution vector.
        :return: the format pattern.
        :rtype: str
        """
        pass

    def repair(self, solution):
        return solution
