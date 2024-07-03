# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from SphereFunction import SphereFunctionProblem
from epiga.epigeneticexception import EpigeneticException


class FloatProblemTestCase(unittest.TestCase):

    def my_setUp(self, size):
        self.size = size
        self.p = SphereFunctionProblem(size, 1)

    def test_size(self):
        for i in range(100):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (self.p.size == i)

    def test_generate_solution(self):
        for i in range(100):
            with self.subTest(i=i):
                self.my_setUp(i)

                v = self.p.generate_solution()
                assert (len(v) == i)

    def test_repair(self):
        for i in range(100):
            with self.subTest(i=i):
                self.my_setUp(i)

                s = self.p.generate_solution()
                sr = self.p.repair(s)
                assert s == sr

    def test_evaluations(self):
        for i in range(100):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (self.p.evaluations == 0)

                try:
                    self.p.compute_fitness([0] * (i + 1))
                    assert False
                except EpigeneticException:
                    pass

                minimum = [0] * i
                known = [1] * i

                assert (self.p.compute_fitness(minimum) == 0)
                assert (self.p.compute_fitness(known) == i)

                assert (self.p.evaluations == 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
