# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from EggholderFunction import EggholderFunctionProblem
from epiga.epigeneticexception import EpigeneticException


class IntegerProblemTestCase(unittest.TestCase):

    def setUp(self):
        self.p = EggholderFunctionProblem(1)

    def test_size(self):
        assert self.p.size == 2

    def test_generate_solution(self):
        v = self.p.generate_solution()
        assert len(v) == 2

    def test_repair(self):
        for i in range(100):
            with self.subTest(i=i):
                s = self.p.generate_solution()
                sr = self.p.repair(s)
                assert s == sr

    def test_evaluations(self):
        assert (self.p.evaluations == 0)

        try:
            self.p.compute_fitness([0])
            assert False
        except EpigeneticException:
            pass

        assert self.p.compute_fitness([0, 0]) == -25.460337185286313
        assert self.p.evaluations == 1

        assert self.p.compute_fitness([1, 1]) == -30.761412199195277
        assert self.p.evaluations == 2


if __name__ == '__main__':
    unittest.main(verbosity=2)
