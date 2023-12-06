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
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.nucleosomegenerator import NucleosomeGenerator


class NucleosomeGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        random.seed(1)
        self.p = OneMaxProblem(10)
        self.pop = EpigeneticPopulation(self.p)
        self.pop.generate(1, 1)

    def test_init(self):
        ng = NucleosomeGenerator(1.0, 10)
        ng.generate(self.pop)
        ind = self.pop.get(0)
        cell = ind.cells[0]
        v1 = cell.nucleosomes[:]
        assert (len(v1) == self.p.size)
        assert (v1 == [True] * self.p.size)

        ng = NucleosomeGenerator(0.0, 10)
        ng.generate(self.pop)
        ind = self.pop.get(0)
        cell = ind.cells[0]
        v2 = cell.nucleosomes[:]
        assert (len(v2) == self.p.size)
        assert (v2 == [False] * self.p.size)

        for i in range(50):
            with self.subTest(i=i):
                ng = NucleosomeGenerator(0.5, 0)
                ng.generate(self.pop)
                ind = self.pop.get(0)
                cell = ind.cells[0]
                v3 = cell.nucleosomes[:]

                assert (len(v3) == self.p.size)
                assert (v3 != v1)
                assert (v3 != v2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
