# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import random
import unittest

from SphereFunction import SphereFunctionProblem
from epiga.epigeneticcell import EpigeneticCell
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.numericgenesilencing import NumericGeneSilencing


class NumericGeneSilencingTestCase(unittest.TestCase):

    def setUp(self):
        self.p = SphereFunctionProblem(10, 1)

    def test_methylate_1(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                c1 = EpigeneticCell(self.p)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = NumericGeneSilencing(0.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution == c1.solution)

    def test_methylate_2(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                v = [0] * 10
                c1 = EpigeneticCell(self.p, nucleosomes=v)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = NumericGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution == c1.solution)

    def test_methylate_3(self):
        for i in range(0, 50):
            with self.subTest(i=i):
                pop = EpigeneticPopulation(self.p)
                v1 = [1] * 10
                v2 = [True] * 10
                c1 = EpigeneticCell(self.p, solution=v1, nucleosomes=v2)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                pop.add(i1)
                gs = NumericGeneSilencing(0.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell() == c1)
                assert (pop.get(0).get_best_cell().solution == v1)

                gs = NumericGeneSilencing(1.0)
                gs.methylate(pop)
                assert (pop.get(0).get_best_cell().solution != v1)
                assert (pop.get(0).get_best_cell() is i1.get_best_cell())
                assert (pop.get(0).get_best_cell() is c1)


if __name__ == '__main__':
    random.seed(3)
    unittest.main(verbosity=2)
