# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import random
import unittest

from OneMax import OneMaxProblem
from epiga.epigeneticcell import EpigeneticCell
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.binarygenesilencing import BinaryGeneSilencing


class NumericGeneSilencingTestCase(unittest.TestCase):

    def setUp(self):
        self.p = OneMaxProblem(10)

    def test_methylate_1(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                c1 = EpigeneticCell(self.p)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = BinaryGeneSilencing(0.0)
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
                gs = BinaryGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution == c1.solution)

    def test_methylate_3(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                v1 = [True] * 10
                c1 = EpigeneticCell(self.p, solution=v1, nucleosomes=v1)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = BinaryGeneSilencing(0.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell() == c1)
                assert (pop.get(0).get_best_cell().solution == v1)

                v2 = [False] * 10
                gs = BinaryGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution != v2)
                assert (pop.get(0).get_best_cell() is i1.get_best_cell())
                assert (pop.get(0).get_best_cell() is c1)


if __name__ == '__main__':
    random.seed(3)
    unittest.main(verbosity=2)
