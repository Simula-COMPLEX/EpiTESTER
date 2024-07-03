# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from TSP import TSP
from epiga.epigeneticexception import EpigeneticException


class PermutationProblemTestCase(unittest.TestCase):

    def setUp(self):
        self.M = [
            [0, 2, 4, 6, 7, 10],
            [2, 0, 6, 5, 4, 3],
            [4, 6, 0, 3, 5, 1],
            [6, 5, 3, 0, 7, 3],
            [7, 4, 5, 7, 0, 9],
            [10, 3, 1, 3, 9, 0],
        ]
        self.p = TSP(self.M)

    def test_size(self):
        assert self.p.size == len(self.M[0])

    def test_generate_solution(self):
        for i in range(100):
            with self.subTest(i=i):
                s = self.p.generate_solution()
                ss = sorted(s)
                assert ss == list(range(len(self.M[0])))

    def test_repair(self):
        v = [0, 1, 2, 3, 4, 5]
        vr = self.p.repair(v)
        assert v == vr

        v = [0, 1, 1, 2, 3, 4]
        vr = self.p.repair(v)
        assert vr == [0, 1, 2, 3, 4, 5]

        v = [1, 1, 2, 3, 4, 0]
        vr = self.p.repair(v)
        assert vr == [0, 2, 3, 4, 1, 5]

        v = [0, 0, 0, 0, 0, 0]
        vr = self.p.repair(v)
        assert vr == [0, 1, 2, 3, 4, 5]

    def test_evaluations(self):
        assert (self.p.evaluations == 0)

        v = [0, 1, 2, 3, 4]
        try:
            self.p.compute_fitness(v)
            assert False
        except EpigeneticException:
            pass

        v = [0, 1, 2, 3, 4, 5]
        assert (self.p.compute_fitness(v) == 37)
        assert (self.p.evaluations == 1)

        v = [0, 5, 4, 3, 2, 1]
        assert (self.p.compute_fitness(v) == 37)
        assert (self.p.evaluations == 2)

        v = [0, 4, 2, 5, 1, 3]
        assert (self.p.compute_fitness(v) == 27)
        assert (self.p.evaluations == 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
