# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import random
import unittest

from TSP import TSP
from epiga.epigeneticcell import EpigeneticCell
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.permutationgenesilencing import PermutationGeneSilencing


class PermutationGeneSilencingTestCase(unittest.TestCase):

    def setUp(self):
        M = [
            [0, 2, 4, 6, 7, 10],
            [2, 0, 6, 5, 4, 3],
            [4, 6, 0, 3, 5, 1],
            [6, 5, 3, 0, 7, 3],
            [7, 4, 5, 7, 0, 9],
            [10, 3, 1, 3, 9, 0],
        ]
        self.p = TSP(M)

    def test_methylate_1(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                c1 = EpigeneticCell(self.p)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = PermutationGeneSilencing(0.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution == c1.solution)

    def test_methylate_2(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                v = [False] * 10
                c1 = EpigeneticCell(self.p, nucleosomes=v)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = PermutationGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution == c1.solution)

    def test_methylate_3(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                v1 = [True] * 10
                s1 = list(range(self.p.size))
                c1 = EpigeneticCell(self.p, solution=s1, nucleosomes=v1)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = PermutationGeneSilencing(0.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell() == c1)
                assert (pop.get(0).get_best_cell().solution == s1)

                s2 = s1[1:]
                random.shuffle(s2)
                s2.insert(0, s1[0])
                gs = PermutationGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution != s2)
                assert (pop.get(0).get_best_cell() is i1.get_best_cell())
                assert (pop.get(0).get_best_cell() is c1)


if __name__ == '__main__':
    random.seed(3)
    unittest.main(verbosity=2)
